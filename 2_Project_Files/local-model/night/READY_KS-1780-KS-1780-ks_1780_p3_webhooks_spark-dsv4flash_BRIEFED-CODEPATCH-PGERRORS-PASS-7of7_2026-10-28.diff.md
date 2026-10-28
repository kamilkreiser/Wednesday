# READY — KS-1780-KS-1780-ks_1780_p3_webhooks (Spark (DeepSeek V4 Flash), briefed, code_patch, jest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1780_p3_webhooks/out.md.checker/patch.diff`** (from `ls` at 13:50 2026-10-28; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1780_p3_webhooks/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1780_p3_webhooks/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1780_p3_webhooks/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1780_p3_webhooks-control-r2/out.md.checker/patch.diff` rc 0, Wednesday).

**Held 13:50 2026-10-28 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1780_p3_webhooks/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `8894c7486f82f6eb682fecb879791f53312537b1`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 touched-file set == { Blockchain/Dev/services/originate/src/utils/pgErrors.ts , Blockchain/Dev/services/originate/src/__tests__/ks1780-extract-pg-code-cannot-hang-a-webhook-patch.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/originate/src/utils/pgErrors.ts` (product) and `Blockchain/Dev/services/originate/src/__tests__/ks1780-extract-pg-code-cannot-hang-a-webhook-patch.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
10	0	Blockchain/Dev/services/originate/src/utils/pgErrors.ts
126	0	Blockchain/Dev/services/originate/src/__tests__/ks1780-extract-pg-code-cannot-hang-a-webhook-patch.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the product hunk (9 line(s)), and no tip line is re-added as a '+' (A3d)` — product section `+` lines 10 ordered-equal (whitespace-stripped) to the brief's `expected_plus` (ASCII); `-` lines 0.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: every '+' line the brief adds is in the applied Blockchain/Dev/services/originate/src/utils/pgErrors.ts byte-exact incl. leading whitespace (apply mode strict): OK 9 line(s) byte-exact incl. leading whitespace (of 9; 10 line(s) added by the apply)` [a3i_indent.out: `OK 9 line(s) byte-exact incl. leading whitespace (of 9; 10 line(s) added by the apply)`]
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/originate/src/utils/pgErrors.ts` (hunks=1, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/originate/src/__tests__/ks1780-extract-pg-code-cannot-hang-a-webhook-patch.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: src/__tests__/ks1780-extract-pg-code-cannot-hang-a-webhook-patch.test.ts fails at the untouched tip (4 failed / 8 run; controls green; assertion reds)` [red_first.json: failed=4 of total=8; red cell(s): ['KS-1780: PATCH /api/webhooks/:id and extractPgCode answer a hostile thrown value RED KS-1780 B1 a revoked Proxy thrown by the update is answered with the constant 500', 'KS-1780: PATCH /api/webhooks/:id and extractPgCode answer a hostile thrown value RED KS-1780 B2 an object whose code getter throws is answered with the constant 500', 'KS-1780: PATCH /api/webhooks/:id and extractPgCode answer a hostile thrown value RED KS-1780 B3 extractPgCode of a revoked Proxy is undefined, not a throw', 'KS-1780: PATCH /api/webhooks/:id and extractPgCode answer a hostile thrown value RED KS-1780 B4 extractPgCode of an object whose meta getter throws is undefined, not a throw']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: src/__tests__/ks1780-extract-pg-code-cannot-hang-a-webhook-patch.test.ts passes with the product hunk (8 passed / 8 run)` [green_after.json: failed=0 of total=8, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=1690 failed=0 | after: total=1698 failed=0` · `NEW reds: []` [baseline_suite.json total=1690 failed=0; after_suite.json total=1698 failed=0]
- A6 [verbatim]: `PASS A6 whole services/originate suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/originate: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 +136/-0 test=src/__tests__/ks1780-extract-pg-code-cannot-hang-a-webhook-patch.test.ts red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/originate/src/utils/pgErrors.ts` (+10/-0 per numstat.out) and the test file `Blockchain/Dev/services/originate/src/__tests__/ks1780-extract-pg-code-cannot-hang-a-webhook-patch.test.ts` (+126/-0); two files. Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `8894c7486f82f6eb682fecb879791f53312537b1` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1780_p3_webhooks/input.json`. brief NOT LOCATED under night/briefs/ (no claim made). Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1780_p3_webhooks/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/originate/src/utils/pgErrors.ts b/Blockchain/Dev/services/originate/src/utils/pgErrors.ts
--- a/Blockchain/Dev/services/originate/src/utils/pgErrors.ts
+++ b/Blockchain/Dev/services/originate/src/utils/pgErrors.ts
@@ -50,6 +50,16 @@
  * if (pgCode === '23503') return res.status(404).json(...);
  */
 export function extractPgCode(err: unknown): string | undefined {
+  // KS-1780: the reads below touch the thrown value (`code`, `meta.code`, `message`). A revoked Proxy, or an object whose getter throws, makes one of them throw. The route catches that call
+  // this function BEFORE they reach fail500 (webhooks.ts PATCH /:id), so the throw rejected the handler's promise and the request got no answer. A value that cannot be read has no code.
+  try {
+    return readPgCode(err);
+  } catch {
+    return undefined;
+  }
+}
+
+function readPgCode(err: unknown): string | undefined {
   const e = err as
     | { code?: unknown; meta?: { code?: unknown }; message?: unknown }
     | null
diff --git a/Blockchain/Dev/services/originate/src/__tests__/ks1780-extract-pg-code-cannot-hang-a-webhook-patch.test.ts b/Blockchain/Dev/services/originate/src/__tests__/ks1780-extract-pg-code-cannot-hang-a-webhook-patch.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/originate/src/__tests__/ks1780-extract-pg-code-cannot-hang-a-webhook-patch.test.ts
@@ -0,0 +1,126 @@
+// KS-1780 (originate routes/webhooks.ts PATCH /:id, utils/pgErrors.ts): the catch of PATCH /api/webhooks/:id called `extractPgCode(err)` BEFORE it reached fail500. extractPgCode reads
+// `code`, `meta.code` and `message` of the thrown value with no try of its own, so a revoked Proxy, or an object whose `code` getter throws, made the call throw inside the catch: the
+// handler's promise rejected and the request got NO answer. B1/B2 drive the real route over a loopback listener and read what the caller gets (a request with no answer in 1500 ms is
+// reported as the string NO ANSWER, so a hang is a red assertion, not a stuck run); B3/B4 pin the helper itself. C1 to C4 keep the KS-445 classification exactly as it was.
+const mockExecuteRawUnsafe = jest.fn();
+
+jest.mock('../db', () => ({
+  prisma: {
+    $queryRaw: jest.fn(),
+    $executeRaw: jest.fn(),
+    $executeRawUnsafe: mockExecuteRawUnsafe,
+  },
+}));
+
+jest.mock('../middleware/auth', () => ({
+  authenticate: () => (_req: unknown, _res: unknown, next: () => void) => next(),
+}));
+
+jest.mock('../utils/logger', () => ({
+  logger: { info: jest.fn(), warn: jest.fn(), error: jest.fn(), debug: jest.fn() },
+}));
+
+import express from 'express';
+import type { AddressInfo } from 'net';
+import { webhooksRouter } from '../routes/webhooks';
+import { extractPgCode } from '../utils/pgErrors';
+
+const WEBHOOK_ID = 'a1b2c3d4-5678-4abc-9def-0123456789ab';
+const CONSTANT_BODY = { success: false, error: { code: 'INTERNAL_ERROR', message: 'Internal server error' } };
+
+const app = express();
+app.use('/api/webhooks', express.json(), webhooksRouter);
+let server: ReturnType<typeof app.listen>;
+let baseUrl = '';
+
+beforeAll(async () => {
+  await new Promise<void>((resolve) => {
+    server = app.listen(0, '127.0.0.1', () => resolve());
+  });
+  baseUrl = 'http://127.0.0.1:' + (server.address() as AddressInfo).port;
+});
+afterAll(() => {
+  (server as unknown as { closeAllConnections?: () => void })?.closeAllConnections?.();
+  server?.close();
+});
+beforeEach(() => mockExecuteRawUnsafe.mockReset());
+
+async function patchWithThrow(thrown: unknown): Promise<{ status: number | 'NO ANSWER'; body: unknown }> {
+  mockExecuteRawUnsafe.mockRejectedValueOnce(thrown);
+  try {
+    const res = await fetch(baseUrl + '/api/webhooks/' + WEBHOOK_ID, {
+      method: 'PATCH',
+      headers: { 'content-type': 'application/json' },
+      body: JSON.stringify({ isActive: true }),
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
+function pgCodeOrThrew(err: unknown): string | undefined {
+  try {
+    return extractPgCode(err);
+  } catch {
+    return 'THREW';
+  }
+}
+
+function throwingCodeGetter(): object {
+  return {
+    get code(): string {
+      throw new Error('ks1780 code getter');
+    },
+  };
+}
+
+describe('KS-1780: PATCH /api/webhooks/:id and extractPgCode answer a hostile thrown value', () => {
+  it('RED KS-1780 B1 a revoked Proxy thrown by the update is answered with the constant 500', async () => {
+    expect(await patchWithThrow(revokedProxy())).toEqual({ status: 500, body: CONSTANT_BODY });
+  });
+
+  it('RED KS-1780 B2 an object whose code getter throws is answered with the constant 500', async () => {
+    expect(await patchWithThrow(throwingCodeGetter())).toEqual({ status: 500, body: CONSTANT_BODY });
+  });
+
+  it('RED KS-1780 B3 extractPgCode of a revoked Proxy is undefined, not a throw', () => {
+    expect(pgCodeOrThrew(revokedProxy())).toBeUndefined();
+  });
+
+  it('RED KS-1780 B4 extractPgCode of an object whose meta getter throws is undefined, not a throw', () => {
+    const hostile = {
+      get meta(): { code: string } {
+        throw new Error('ks1780 meta getter');
+      },
+    };
+    expect(pgCodeOrThrew(hostile)).toBeUndefined();
+  });
+
+  it('control KS-1780 C1 a Prisma-wrapped 42804 is still answered 400 VALIDATION_ERROR', async () => {
+    const reply = await patchWithThrow(Object.assign(new Error('Raw query failed.'), { code: 'P2010', meta: { code: '42804' } }));
+    expect(reply.status).toBe(400);
+    expect((reply.body as { error: { code: string } }).error.code).toBe('VALIDATION_ERROR');
+  });
+
+  it('control KS-1780 C2 a bare pg 23514 on code is still answered 400 VALIDATION_ERROR', async () => {
+    const reply = await patchWithThrow({ code: '23514' });
+    expect(reply.status).toBe(400);
+    expect((reply.body as { error: { code: string } }).error.code).toBe('VALIDATION_ERROR');
+  });
+
+  it('control KS-1780 C3 an ordinary Error is still answered with the constant 500', async () => {
+    expect(await patchWithThrow(new Error('connection terminated unexpectedly'))).toEqual({ status: 500, body: CONSTANT_BODY });
+  });
+
+  it('control KS-1780 C4 extractPgCode still reads a known code out of the message text', () => {
+    expect(extractPgCode(new Error('Raw query failed. Code: `22P02`. Message: `invalid input syntax`'))).toBe('22P02');
+  });
+});
```
