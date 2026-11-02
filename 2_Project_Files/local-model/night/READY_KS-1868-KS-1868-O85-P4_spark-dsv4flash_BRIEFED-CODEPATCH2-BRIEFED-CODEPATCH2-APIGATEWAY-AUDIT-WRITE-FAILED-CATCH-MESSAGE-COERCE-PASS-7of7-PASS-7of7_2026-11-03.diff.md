# READY — KS-1868-KS-1868-O85-P4 (spark-dsv4flash, briefed, code_patch2, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o85_p4_api_gateway_audit_write_failed_catch_guard_message/out.md.checker/patch.diff`** (from `ls` at 00:08 2026-11-03; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o85_p4_api_gateway_audit_write_failed_catch_guard_message/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o85_p4_api_gateway_audit_write_failed_catch_guard_message/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o85_p4_api_gateway_audit_write_failed_catch_guard_message/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o85_p4_api_gateway_audit_write_failed_catch_guard_message-control-r3/out.md.checker/patch.diff` rc 0, Wednesday).

**Held 00:08 2026-11-03 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o85_p4_api_gateway_audit_write_failed_catch_guard_message/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `3043c5bcf4e9f437c8caf2594caaaeab284c59a8`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/services/api-gateway/src/middleware/audit.ts } + { Blockchain/Dev/services/api-gateway/src/__tests__/ks1868-audit-write-failed-catch-unreadable-throw.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/api-gateway/src/middleware/audit.ts` (product) and `Blockchain/Dev/services/api-gateway/src/__tests__/ks1868-audit-write-failed-catch-unreadable-throw.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
7	1	Blockchain/Dev/services/api-gateway/src/middleware/audit.ts
157	0	Blockchain/Dev/services/api-gateway/src/__tests__/ks1868-audit-write-failed-catch-unreadable-throw.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (7 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: audit.ts`
- CODE_PATCH2 (rung 3, 1 product files + 1 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/services/api-gateway/src/middleware/audit.ts`; test(s): `Blockchain/Dev/services/api-gateway/src/__tests__/ks1868-audit-write-failed-catch-unreadable-throw.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/services/api-gateway/src/middleware/audit.ts 7 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/api-gateway/src/__tests__/ks1868-audit-write-failed-catch-unreadable-throw.test.ts 157 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/api-gateway/src/middleware/audit.ts` (hunks=1, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/api-gateway/src/__tests__/ks1868-audit-write-failed-catch-unreadable-throw.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (4 failed / 8 run; controls green; assertion reds)` [red_first.json: failed=4 of total=8; red cell(s): ['KS-1868 the audit write-failed catch logs text for a hostile thrown value RED ks1868 R1: an INSERT rejection that is a revoked Proxy is logged as a warning with the error as text and the entry path, as for an ordinary Error', 'KS-1868 the audit write-failed catch logs text for a hostile thrown value RED ks1868 R2: an INSERT rejection that is an Error whose message getter throws is logged as a warning with the error as text and the entry path, as for an ordinary Error', 'KS-1868 the audit write-failed catch logs text for a hostile thrown value RED ks1868 R3: an INSERT rejection that is an Error whose message is a null-prototype object is logged as a warning with the error as text and the entry path, as for an ordinary Error', 'KS-1868 the audit write-failed catch logs text for a hostile thrown value RED ks1868 R4: an INSERT rejection that is an Error whose message is a Symbol is logged as a warning with the error as text and the entry path, as for an ordinary Error']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 1 product section(s) (8 passed / 8 run)` [green_after.json: failed=0 of total=8, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=1412 failed=2 | after: total=1420 failed=0` · `NEW reds: []` [baseline_suite.json total=1412 failed=2; after_suite.json total=1420 failed=0]
- A6 [verbatim]: `PASS A6 whole services/api-gateway suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/api-gateway: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 products=1 tests=1 red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/api-gateway/src/middleware/audit.ts` (+7/-1 per numstat.out) and the test file `Blockchain/Dev/services/api-gateway/src/__tests__/ks1868-audit-write-failed-catch-unreadable-throw.test.ts` (+157/-0); 2 files in all (code_patch2: products Blockchain/Dev/services/api-gateway/src/middleware/audit.ts). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `3043c5bcf4e9f437c8caf2594caaaeab284c59a8` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o85_p4_api_gateway_audit_write_failed_catch_guard_message/input.json`. Brief (given by --brief; its `# ` heading names KS-1868): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1868_o85_p4_api_gateway_audit_write_failed_catch_guard_message/KS-1868.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o85_p4_api_gateway_audit_write_failed_catch_guard_message/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/api-gateway/src/middleware/audit.ts b/Blockchain/Dev/services/api-gateway/src/middleware/audit.ts
--- a/Blockchain/Dev/services/api-gateway/src/middleware/audit.ts
+++ b/Blockchain/Dev/services/api-gateway/src/middleware/audit.ts
@@ -330,8 +330,14 @@
             ],
           ));
         } catch (err) {
+          let reason: string;
+          try {
+            reason = String(err instanceof Error ? err.message : err);
+          } catch {
+            reason = 'unreadable thrown value';
+          }
           deps.log('warn', 'audit middleware: write failed', {
-            error: err instanceof Error ? err.message : String(err),
+            error: reason,
             path: auditPath, // KS-1457: was req.path, the trimmed remainder behind a responding gate
           });
         }
diff --git a/Blockchain/Dev/services/api-gateway/src/__tests__/ks1868-audit-write-failed-catch-unreadable-throw.test.ts b/Blockchain/Dev/services/api-gateway/src/__tests__/ks1868-audit-write-failed-catch-unreadable-throw.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/api-gateway/src/__tests__/ks1868-audit-write-failed-catch-unreadable-throw.test.ts
@@ -0,0 +1,157 @@
+import { describe, it, expect, afterEach } from 'vitest';
+import express from 'express';
+import http from 'node:http';
+import type { AddressInfo } from 'node:net';
+import { createAuditMiddleware } from '../middleware/audit';
+
+// KS-1868 (operator 85 screen, gateway audit): the catch of the fire-and-forget audit write in
+// services/api-gateway/src/middleware/audit.ts logs `{ error: err instanceof Error ? err.message : String(err) }` with the read
+// INSIDE the log call's arguments, unguarded. A thrown value whose read throws (a revoked Proxy: `instanceof` throws; an Error
+// whose message getter throws) makes the catch itself throw, so the async IIFE that nothing awaits REJECTS: an unhandled
+// rejection and no warning line, so the lost audit row leaves no trace; an Error whose message is readable but not a string
+// is handed to the log as is. The cells make the INSERT reject with such a value and assert the warning line is written with
+// the error as text (the constant when the value cannot be turned into text) and the entry path. Harness: the real
+// middleware on a real express app on loopback with plain-function dependencies (no database).
+type LogCall = { level: string; msg: string; ctx: Record<string, unknown> | undefined };
+
+const servers: http.Server[] = [];
+afterEach(async () => {
+  while (servers.length) {
+    const s = servers.pop()!;
+    s.closeAllConnections();
+    await new Promise<void>((r) => s.close(() => r()));
+  }
+});
+
+async function drive(query: () => Promise<{ rows: unknown[] }>): Promise<{ logs: LogCall[]; queries: () => number }> {
+  const logs: LogCall[] = [];
+  let calls = 0;
+  const app = express();
+  app.use(express.json());
+  app.use(
+    createAuditMiddleware({
+      query: () => {
+        calls += 1;
+        return query();
+      },
+      isDbAvailable: () => true,
+      log: (level: string, msg: string, ctx?: object) => {
+        logs.push({ level, msg, ctx: ctx as Record<string, unknown> | undefined });
+      },
+    } as unknown as Parameters<typeof createAuditMiddleware>[0]),
+  );
+  app.post('/api/auth/login', (_req, res) => {
+    res.status(401).json({ error: 'no' });
+  });
+  const server = app.listen(0, '127.0.0.1');
+  servers.push(server);
+  await new Promise<void>((r) => server.once('listening', () => r()));
+  const port = (server.address() as AddressInfo).port;
+  await new Promise<void>((resolve, reject) => {
+    const req = http.request(
+      { host: '127.0.0.1', port, path: '/api/auth/login', method: 'POST', headers: { 'content-type': 'application/json' } },
+      (res) => {
+        res.resume();
+        res.on('end', () => resolve());
+      },
+    );
+    req.on('error', reject);
+    req.end(JSON.stringify({ email: 'a@ks1868.test' }));
+  });
+  return { logs, queries: () => calls };
+}
+
+/** Waits until cond() holds or the timeout passes; never throws, so the assertion after it is what fails. */
+async function until(cond: () => boolean, _what: string, timeout = 1500): Promise<void> {
+  const start = Date.now();
+  while (Date.now() - start < timeout) {
+    if (cond()) return;
+    await new Promise((r) => setTimeout(r, 20));
+  }
+}
+
+const FAILED = 'audit middleware: write failed';
+const failedLines = (logs: LogCall[]) => logs.filter((l) => l.msg === FAILED);
+/** The logged `error` field as a string; the type name when it is not one (a hostile value never reaches an assertion). */
+const reasonOf = (l: LogCall | undefined): string => {
+  const v = l?.ctx?.error;
+  return typeof v === 'string' ? v : '<' + typeof v + '>';
+};
+const rejecting = (v: unknown) => () => Promise.reject(v);
+
+const revokedProxy = (): unknown => {
+  const rp = Proxy.revocable({}, {});
+  rp.revoke();
+  return rp.proxy;
+};
+/** An Error whose `message` getter succeeds and returns the value m. */
+const withMessage = (m: unknown): unknown => Object.create(Error.prototype, { message: { get() { return m; } } });
+const getterThrows = (): unknown =>
+  Object.create(Error.prototype, {
+    message: {
+      get() {
+        throw new Error('getter boom');
+      },
+    },
+  });
+const SHAPES: Array<[string, () => unknown, string]> = [
+  ['a revoked Proxy', revokedProxy, 'unreadable thrown value'],
+  ['an Error whose message getter throws', getterThrows, 'unreadable thrown value'],
+  ['an Error whose message is a null-prototype object', () => withMessage(Object.create(null)), 'unreadable thrown value'],
+  ['an Error whose message is a Symbol', () => withMessage(Symbol('ks1868')), 'Symbol(ks1868)'],
+];
+
+describe('KS-1868 the audit write-failed catch logs text for a hostile thrown value', () => {
+  it('control ks1868 C1: an ordinary Error is logged as a warning with its message and the entry path', async () => {
+    const r = await drive(rejecting(new Error('ks1868 boom')));
+    await until(() => failedLines(r.logs).length > 0, 'the write-failed warning');
+    expect(failedLines(r.logs)).toHaveLength(1);
+    expect(failedLines(r.logs)[0].level).toBe('warn');
+    expect(reasonOf(failedLines(r.logs)[0])).toBe('ks1868 boom');
+    expect(failedLines(r.logs)[0].ctx?.path).toBe('/api/auth/login');
+  });
+  it('control ks1868 C2: a thrown plain string is logged as its own text', async () => {
+    const r = await drive(rejecting('plain boom'));
+    await until(() => failedLines(r.logs).length > 0, 'the write-failed warning');
+    expect(reasonOf(failedLines(r.logs)[0])).toBe('plain boom');
+  });
+  it('control ks1868 C3: a thrown number is logged as its text', async () => {
+    const r = await drive(rejecting(42));
+    await until(() => failedLines(r.logs).length > 0, 'the write-failed warning');
+    expect(reasonOf(failedLines(r.logs)[0])).toBe('42');
+  });
+  it('control ks1868 C4: a write that succeeds logs no write-failed line', async () => {
+    const r = await drive(() => Promise.resolve({ rows: [] }));
+    await until(() => r.queries() > 0, 'the audit write');
+    await new Promise((x) => setTimeout(x, 100));
+    expect(failedLines(r.logs)).toHaveLength(0);
+  });
+  it('RED ks1868 R1: an INSERT rejection that is a revoked Proxy is logged as a warning with the error as text and the entry path, as for an ordinary Error', async () => {
+    const r = await drive(rejecting(SHAPES[0][1]()));
+    await until(() => failedLines(r.logs).length > 0, 'the write-failed warning');
+    expect(failedLines(r.logs)).toHaveLength(1);
+    expect(reasonOf(failedLines(r.logs)[0])).toBe(SHAPES[0][2]);
+    expect(failedLines(r.logs)[0].ctx?.path).toBe('/api/auth/login');
+  });
+  it('RED ks1868 R2: an INSERT rejection that is an Error whose message getter throws is logged as a warning with the error as text and the entry path, as for an ordinary Error', async () => {
+    const r = await drive(rejecting(SHAPES[1][1]()));
+    await until(() => failedLines(r.logs).length > 0, 'the write-failed warning');
+    expect(failedLines(r.logs)).toHaveLength(1);
+    expect(reasonOf(failedLines(r.logs)[0])).toBe(SHAPES[1][2]);
+    expect(failedLines(r.logs)[0].ctx?.path).toBe('/api/auth/login');
+  });
+  it('RED ks1868 R3: an INSERT rejection that is an Error whose message is a null-prototype object is logged as a warning with the error as text and the entry path, as for an ordinary Error', async () => {
+    const r = await drive(rejecting(SHAPES[2][1]()));
+    await until(() => failedLines(r.logs).length > 0, 'the write-failed warning');
+    expect(failedLines(r.logs)).toHaveLength(1);
+    expect(reasonOf(failedLines(r.logs)[0])).toBe(SHAPES[2][2]);
+    expect(failedLines(r.logs)[0].ctx?.path).toBe('/api/auth/login');
+  });
+  it('RED ks1868 R4: an INSERT rejection that is an Error whose message is a Symbol is logged as a warning with the error as text and the entry path, as for an ordinary Error', async () => {
+    const r = await drive(rejecting(SHAPES[3][1]()));
+    await until(() => failedLines(r.logs).length > 0, 'the write-failed warning');
+    expect(failedLines(r.logs)).toHaveLength(1);
+    expect(reasonOf(failedLines(r.logs)[0])).toBe(SHAPES[3][2]);
+    expect(failedLines(r.logs)[0].ctx?.path).toBe('/api/auth/login');
+  });
+});
```
