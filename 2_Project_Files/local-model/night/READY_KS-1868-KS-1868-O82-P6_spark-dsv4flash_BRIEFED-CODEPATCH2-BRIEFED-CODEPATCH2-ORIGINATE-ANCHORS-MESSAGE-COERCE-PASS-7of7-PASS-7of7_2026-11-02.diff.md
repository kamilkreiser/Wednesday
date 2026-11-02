# READY — KS-1868-KS-1868-O82-P6 (spark-dsv4flash, briefed, code_patch2, jest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o82_p6_originate_anchors_catches_coerce_message/out.md.checker/patch.diff`** (from `ls` at 21:07 2026-11-02; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o82_p6_originate_anchors_catches_coerce_message/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o82_p6_originate_anchors_catches_coerce_message/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o82_p6_originate_anchors_catches_coerce_message/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o82_p6_originate_anchors_catches_coerce_message-control-r2/out.md.checker/patch.diff` rc 0, Wednesday).

**Held 21:07 2026-11-02 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o82_p6_originate_anchors_catches_coerce_message/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `0e3a9b65cdd632fbc1783257c6cb9833934e1404`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/services/originate/src/routes/anchors.ts } + { Blockchain/Dev/services/originate/src/__tests__/ks1868-anchors-message-coercion-unreadable-throw.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/originate/src/routes/anchors.ts` (product) and `Blockchain/Dev/services/originate/src/__tests__/ks1868-anchors-message-coercion-unreadable-throw.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
3	3	Blockchain/Dev/services/originate/src/routes/anchors.ts
199	0	Blockchain/Dev/services/originate/src/__tests__/ks1868-anchors-message-coercion-unreadable-throw.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (3 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: anchors.ts`
- CODE_PATCH2 (rung 3, 1 product files + 1 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/services/originate/src/routes/anchors.ts`; test(s): `Blockchain/Dev/services/originate/src/__tests__/ks1868-anchors-message-coercion-unreadable-throw.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/services/originate/src/routes/anchors.ts 3 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/originate/src/__tests__/ks1868-anchors-message-coercion-unreadable-throw.test.ts 199 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/originate/src/routes/anchors.ts` (hunks=3, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/originate/src/__tests__/ks1868-anchors-message-coercion-unreadable-throw.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (8 failed / 12 run; controls green; assertion reds)` [red_first.json: failed=8 of total=12; red cell(s): ['KS-1868 the originate anchor catches log text for a hostile non-string message RED ks1868 R1 GET /:documentId: a rejection whose message is a revoked Proxy logs the constant reason and both lines carry it and the route answers 500', 'KS-1868 the originate anchor catches log text for a hostile non-string message RED ks1868 R2 GET /:documentId: a rejection whose message is an object whose toString throws logs the constant reason and both lines carry it and the route answers 500', 'KS-1868 the originate anchor catches log text for a hostile non-string message RED ks1868 R3 GET /:documentId: a rejection whose message is a null-prototype object logs the constant reason and both lines carry it and the route answers 500', 'KS-1868 the originate anchor catches log text for a hostile non-string message RED ks1868 R4 GET /:documentId: a rejection whose message is a Symbol logs the Symbol text and both lines carry it and the route answers 500', 'KS-1868 the originate anchor catches log text for a hostile non-string message RED ks1868 R5 verifyAnchorsDbReady: a rejection whose message is a revoked Proxy logs the constant reason and the constant error is thrown', 'KS-1868 the originate anchor catches log text for a hostile non-string message RED ks1868 R6 verifyAnchorsDbReady: a rejection whose message is an object whose toString throws logs the constant reason and the constant error is thrown', 'KS-1868 the originate anchor catches log text for a hostile non-string message RED ks1868 R7 verifyAnchorsDbReady: a rejection whose message is a null-prototype object logs the constant reason and the constant error is thrown', 'KS-1868 the originate anchor catches log text for a hostile non-string message RED ks1868 R8 verifyAnchorsDbReady: a rejection whose message is a Symbol logs the Symbol text and the constant error is thrown']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 1 product section(s) (12 passed / 12 run)` [green_after.json: failed=0 of total=12, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=2189 failed=0 | after: total=2201 failed=0` · `NEW reds: []` [baseline_suite.json total=2189 failed=0; after_suite.json total=2201 failed=0]
- A6 [verbatim]: `PASS A6 whole services/originate suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/originate: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 products=1 tests=1 red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/originate/src/routes/anchors.ts` (+3/-3 per numstat.out) and the test file `Blockchain/Dev/services/originate/src/__tests__/ks1868-anchors-message-coercion-unreadable-throw.test.ts` (+199/-0); 2 files in all (code_patch2: products Blockchain/Dev/services/originate/src/routes/anchors.ts). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `0e3a9b65cdd632fbc1783257c6cb9833934e1404` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o82_p6_originate_anchors_catches_coerce_message/input.json`. Brief (given by --brief; its `# ` heading names KS-1868): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1868_o82_p6_originate_anchors_catches_coerce_message/KS-1868.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o82_p6_originate_anchors_catches_coerce_message/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/originate/src/routes/anchors.ts b/Blockchain/Dev/services/originate/src/routes/anchors.ts
--- a/Blockchain/Dev/services/originate/src/routes/anchors.ts
+++ b/Blockchain/Dev/services/originate/src/routes/anchors.ts
@@ -50,7 +50,7 @@
   } catch (err: any) {
     let reason: string;
     try {
-      reason = err instanceof Error ? err.message : String(err);
+      reason = String(err instanceof Error ? err.message : err);
     } catch {
       reason = 'unreadable thrown value';
     }
@@ -96,7 +96,7 @@
   } catch (err: any) {
     let reason: string;
     try {
-      reason = err instanceof Error ? err.message : String(err);
+      reason = String(err instanceof Error ? err.message : err);
     } catch {
       reason = 'unreadable thrown value';
     }
@@ -214,7 +214,7 @@
     } catch (error) {
       let reason: string;
       try {
-        reason = error instanceof Error ? error.message : String(error);
+        reason = String(error instanceof Error ? error.message : error);
       } catch {
         reason = 'unreadable thrown value';
       }
diff --git a/Blockchain/Dev/services/originate/src/__tests__/ks1868-anchors-message-coercion-unreadable-throw.test.ts b/Blockchain/Dev/services/originate/src/__tests__/ks1868-anchors-message-coercion-unreadable-throw.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/originate/src/__tests__/ks1868-anchors-message-coercion-unreadable-throw.test.ts
@@ -0,0 +1,199 @@
+// KS-1868 (QA gate 114, G114-F1 and F2): the originate anchor routes log `error: <reason>` in three catches (getAnchorByDocumentId
+// warn, the GET /:documentId route catch and verifyAnchorsDbReady) where `reason` is `err instanceof Error ? err.message :
+// String(err)`. PR 1932 guards the READ; an Error whose message is readable but not a string (a revoked Proxy, an object whose
+// toString throws, a null-prototype object, a Symbol) passes it to the logger as is, and the real winston throws while formatting
+// it. The cells reject with an Error whose `message` getter RETURNS such a value and assert the logged reason is text (the
+// constant when it cannot be turned into text), the route answers the constant 500 and verifyAnchorsDbReady throws the constant
+// error. G114-F2: the GET uses an abort signal (a hang is a null answer, not a jest timeout), unhandled rejections are counted, and
+// the rejection of verifyAnchorsDbReady is read through a plain `.then(ok, err)` (no jest matcher touches a hostile value).
+// Controls pin a thrown plain string (a non-Error is logged as its own text). Harness: the ks1868 anchors test. Nothing is written.
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
+const toStringThrows = (): unknown => ({
+  toString() {
+    throw new Error('ts boom');
+  },
+});
+/** An Error whose `message` getter succeeds and returns the (non-string) value m. */
+const withMessage = (m: unknown): unknown => Object.create(Error.prototype, { message: { get() { return m; } } });
+/** The logged `error` field of a logger call as a string; the type name when it is not one. */
+const reasonOf = (c: unknown[] | undefined): string => {
+  const v = (c?.[1] as { error?: unknown } | undefined)?.error;
+  return typeof v === 'string' ? v : '<' + typeof v + '>';
+};
+const SHAPES: Array<[string, () => unknown, string]> = [
+  ['a revoked Proxy', revokedProxy, 'unreadable thrown value'],
+  ['an object whose toString throws', toStringThrows, 'unreadable thrown value'],
+  ['a null-prototype object', () => Object.create(null), 'unreadable thrown value'],
+  ['a Symbol', () => Symbol('ks1868'), 'Symbol(ks1868)'],
+];
+
+let unhandled = 0;
+const onUnhandled = () => {
+  unhandled += 1;
+};
+beforeAll(() => {
+  process.on('unhandledRejection', onUnhandled);
+});
+afterAll(() => {
+  process.removeListener('unhandledRejection', onUnhandled);
+});
+beforeEach(() => {
+  unhandled = 0;
+});
+
+async function getAnchor(): Promise<{ status: number; code: string | undefined } | null> {
+  try {
+    const res = await fetch(`${baseUrl}/api/anchors/${DOC}`, { signal: AbortSignal.timeout(1500) });
+    const body = (await res.json()) as { error?: { code?: string } };
+    return { status: res.status, code: body.error?.code };
+  } catch {
+    return null;
+  }
+}
+const readyOutcome = (): Promise<string> =>
+  verifyAnchorsDbReady().then(
+    () => 'resolved',
+    (e: unknown) => (e instanceof Error ? e.message : '<non-error>'),
+  );
+async function route(thrown: unknown, reason: string): Promise<void> {
+  mockState.toThrow = thrown;
+  expect(await getAnchor()).toEqual({ status: 500, code: 'INTERNAL_ERROR' });
+  expect(unhandled).toBe(0);
+  expect(mockState.warned).toHaveLength(1);
+  expect(mockState.warned[0][0]).toBe('Failed to fetch anchor from DB');
+  expect(reasonOf(mockState.warned[0])).toBe(reason);
+  expect(mockState.errored).toHaveLength(1);
+  expect(mockState.errored[0][0]).toBe('Failed to get anchor');
+  expect(reasonOf(mockState.errored[0])).toBe(reason);
+  expect(mockState.writes).toBe(0);
+}
+async function ready(thrown: unknown, reason: string): Promise<void> {
+  mockState.toThrow = thrown;
+  expect(await readyOutcome()).toBe(DB_READY_MESSAGE);
+  expect(mockState.errored).toHaveLength(1);
+  expect(reasonOf(mockState.errored[0])).toBe(reason);
+}
+
+describe('KS-1868 the originate anchor catches log text for a hostile non-string message', () => {
+  it('control ks1868 C1 GET /:documentId: an ordinary Error is logged with its own message on both lines and the route answers 500', async () => {
+    await route(new Error('Connection terminated unexpectedly'), 'Connection terminated unexpectedly');
+  });
+
+  it('control ks1868 C2 verifyAnchorsDbReady: an ordinary Error is logged with its own message and the constant error is thrown', async () => {
+    await ready(new Error('db down'), 'db down');
+  });
+
+  it('control ks1868 C3 GET /:documentId: a thrown plain string is logged as its own text on both lines and the route answers 500', async () => {
+    await route('plain boom', 'plain boom');
+  });
+
+  it('control ks1868 C4 verifyAnchorsDbReady: a thrown plain string is logged as its own text and the constant error is thrown', async () => {
+    await ready('plain boom', 'plain boom');
+  });
+
+  it('RED ks1868 R1 GET /:documentId: a rejection whose message is a revoked Proxy logs the constant reason and both lines carry it and the route answers 500', async () => {
+    await route(withMessage(SHAPES[0][1]()), SHAPES[0][2]);
+  });
+
+  it('RED ks1868 R2 GET /:documentId: a rejection whose message is an object whose toString throws logs the constant reason and both lines carry it and the route answers 500', async () => {
+    await route(withMessage(SHAPES[1][1]()), SHAPES[1][2]);
+  });
+
+  it('RED ks1868 R3 GET /:documentId: a rejection whose message is a null-prototype object logs the constant reason and both lines carry it and the route answers 500', async () => {
+    await route(withMessage(SHAPES[2][1]()), SHAPES[2][2]);
+  });
+
+  it('RED ks1868 R4 GET /:documentId: a rejection whose message is a Symbol logs the Symbol text and both lines carry it and the route answers 500', async () => {
+    await route(withMessage(SHAPES[3][1]()), SHAPES[3][2]);
+  });
+
+  it('RED ks1868 R5 verifyAnchorsDbReady: a rejection whose message is a revoked Proxy logs the constant reason and the constant error is thrown', async () => {
+    await ready(withMessage(SHAPES[0][1]()), SHAPES[0][2]);
+  });
+
+  it('RED ks1868 R6 verifyAnchorsDbReady: a rejection whose message is an object whose toString throws logs the constant reason and the constant error is thrown', async () => {
+    await ready(withMessage(SHAPES[1][1]()), SHAPES[1][2]);
+  });
+
+  it('RED ks1868 R7 verifyAnchorsDbReady: a rejection whose message is a null-prototype object logs the constant reason and the constant error is thrown', async () => {
+    await ready(withMessage(SHAPES[2][1]()), SHAPES[2][2]);
+  });
+
+  it('RED ks1868 R8 verifyAnchorsDbReady: a rejection whose message is a Symbol logs the Symbol text and the constant error is thrown', async () => {
+    await ready(withMessage(SHAPES[3][1]()), SHAPES[3][2]);
+  });
+});
```
