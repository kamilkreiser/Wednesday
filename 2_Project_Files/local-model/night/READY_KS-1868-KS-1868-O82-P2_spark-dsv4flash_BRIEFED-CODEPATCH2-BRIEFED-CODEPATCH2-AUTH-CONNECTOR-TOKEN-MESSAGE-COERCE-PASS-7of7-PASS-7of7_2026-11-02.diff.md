# READY — KS-1868-KS-1868-O82-P2 (spark-dsv4flash, briefed, code_patch2, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o82_p2_auth_internal_connector_token_catch_coerce_message-r2/out.md.checker/patch.diff`** (from `ls` at 21:10 2026-11-02; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o82_p2_auth_internal_connector_token_catch_coerce_message-r2/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o82_p2_auth_internal_connector_token_catch_coerce_message-r2/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o82_p2_auth_internal_connector_token_catch_coerce_message-r2/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o82_p2_auth_internal_connector_token_catch_coerce_message-control/out.md.checker/patch.diff` rc 0, Wednesday).

**Held 21:10 2026-11-02 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o82_p2_auth_internal_connector_token_catch_coerce_message-r2/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `0e3a9b65cdd632fbc1783257c6cb9833934e1404`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/services/auth/src/routes/internal.ts } + { Blockchain/Dev/services/auth/src/__tests__/ks1868-internal-connector-token-message-coercion-unreadable-throw.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/auth/src/routes/internal.ts` (product) and `Blockchain/Dev/services/auth/src/__tests__/ks1868-internal-connector-token-message-coercion-unreadable-throw.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
2	1	Blockchain/Dev/services/auth/src/routes/internal.ts
173	0	Blockchain/Dev/services/auth/src/__tests__/ks1868-internal-connector-token-message-coercion-unreadable-throw.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (2 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: internal.ts`
- CODE_PATCH2 (rung 3, 1 product files + 1 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/services/auth/src/routes/internal.ts`; test(s): `Blockchain/Dev/services/auth/src/__tests__/ks1868-internal-connector-token-message-coercion-unreadable-throw.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/services/auth/src/routes/internal.ts 2 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/auth/src/__tests__/ks1868-internal-connector-token-message-coercion-unreadable-throw.test.ts 173 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/auth/src/routes/internal.ts` (hunks=1, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/auth/src/__tests__/ks1868-internal-connector-token-message-coercion-unreadable-throw.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (4 failed / 7 run; controls green; assertion reds)` [red_first.json: failed=4 of total=7; red cell(s): ['KS-1868 the connector-token catch logs text for a hostile non-string message RED ks1868 R1 : a rejection whose message is a revoked Proxy logs the constant reason and the route answers 502 with no token', 'KS-1868 the connector-token catch logs text for a hostile non-string message RED ks1868 R2 : a rejection whose message is an object whose toString throws logs the constant reason and the route answers 502 with no token', 'KS-1868 the connector-token catch logs text for a hostile non-string message RED ks1868 R3 : a rejection whose message is a null-prototype object logs the constant reason and the route answers 502 with no token', 'KS-1868 the connector-token catch logs text for a hostile non-string message RED ks1868 R4 : a rejection whose message is a Symbol logs the Symbol text and the route answers 502 with no token']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 1 product section(s) (7 passed / 7 run)` [green_after.json: failed=0 of total=7, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=1492 failed=0 | after: total=1499 failed=0` · `NEW reds: []` [baseline_suite.json total=1492 failed=0; after_suite.json total=1499 failed=0]
- A6 [verbatim]: `PASS A6 whole services/auth suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/auth: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 products=1 tests=1 red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/auth/src/routes/internal.ts` (+2/-1 per numstat.out) and the test file `Blockchain/Dev/services/auth/src/__tests__/ks1868-internal-connector-token-message-coercion-unreadable-throw.test.ts` (+173/-0); 2 files in all (code_patch2: products Blockchain/Dev/services/auth/src/routes/internal.ts). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `0e3a9b65cdd632fbc1783257c6cb9833934e1404` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o82_p2_auth_internal_connector_token_catch_coerce_message-r2/input.json`. Brief (given by --brief; its `# ` heading names KS-1868): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1868_o82_p2_auth_internal_connector_token_catch_coerce_message/KS-1868.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o82_p2_auth_internal_connector_token_catch_coerce_message-r2/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/auth/src/routes/internal.ts b/Blockchain/Dev/services/auth/src/routes/internal.ts
--- a/Blockchain/Dev/services/auth/src/routes/internal.ts
+++ b/Blockchain/Dev/services/auth/src/routes/internal.ts
@@ -79,7 +79,8 @@
   } catch (err) {
     let reason: string;
     try {
-      reason = (err as Error).message;
+      const m = (err as Error).message;
+      reason = m === undefined || m === null ? m : String(m);
     } catch {
       reason = 'unreadable thrown value';
     }
diff --git a/Blockchain/Dev/services/auth/src/__tests__/ks1868-internal-connector-token-message-coercion-unreadable-throw.test.ts b/Blockchain/Dev/services/auth/src/__tests__/ks1868-internal-connector-token-message-coercion-unreadable-throw.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/auth/src/__tests__/ks1868-internal-connector-token-message-coercion-unreadable-throw.test.ts
@@ -0,0 +1,173 @@
+import { describe, it, expect, beforeAll, afterAll, beforeEach, vi } from 'vitest';
+import type { AddressInfo } from 'node:net';
+import type { Server } from 'node:http';
+import express from 'express';
+
+// KS-1868 (QA gate 113, G113-F1 and F2): the POST /internal/connector-token catch in routes/internal.ts logs `{ error: reason }`
+// where `reason` is whatever `(err as Error).message` returned, then answers the constant 502 BAD_GATEWAY. PR 1931 guards the
+// READ; a message that is readable but not a string (a revoked Proxy, an object whose toString throws, a null-prototype object,
+// a Symbol) is passed to the logger as is, and the real winston throws while formatting it. The cells make the security call
+// reject with an Error whose `message` getter RETURNS such a value and assert the logged reason is text (the constant when it
+// cannot be turned into text), the 502, no token and no unhandled rejection (the outcome an ordinary Error gets). Controls pin
+// the two shapes no earlier cell pinned: a thrown `undefined` (reading `.message` throws, so the constant) and a thrown plain
+// string (no message: logged with no `error` field, not the text undefined). Harness: the ks1868 connector-token test.
+const realFetch = globalThis.fetch;
+
+const h = vi.hoisted(() => ({
+  toThrow: undefined as unknown,
+  logged: [] as unknown[][],
+  unhandled: 0,
+}));
+
+const capture = vi.hoisted(() => ({
+  debug: () => undefined,
+  info: () => undefined,
+  warn: () => undefined,
+  error: (...args: unknown[]) => {
+    h.logged.push(args);
+  },
+  log: () => undefined,
+}));
+vi.mock('../utils/logger', () => ({ logger: capture, createLogger: () => capture, validateEnv: () => undefined }));
+vi.mock('../services/jwt', () => ({
+  generateConnectorToken: () => ({ token: 'MINTED_1868_CONNECTOR', expiresIn: 300 }),
+}));
+
+const SAVED_LISTENERS = process.listeners('unhandledRejection');
+const onUnhandled = () => {
+  h.unhandled += 1;
+};
+
+let server: Server;
+let baseUrl = '';
+beforeAll(async () => {
+  process.removeAllListeners('unhandledRejection');
+  process.on('unhandledRejection', onUnhandled);
+  globalThis.fetch = ((_input: unknown) => Promise.reject(h.toThrow)) as unknown as typeof fetch;
+  const { internalRoutes } = await import('../routes/internal');
+  const app = express();
+  app.use(express.json());
+  app.use('/internal', internalRoutes);
+  server = app.listen(0, '127.0.0.1');
+  await new Promise<void>((resolve) => server.once('listening', () => resolve()));
+  baseUrl = 'http://127.0.0.1:' + String((server.address() as AddressInfo).port);
+});
+afterAll(async () => {
+  globalThis.fetch = realFetch;
+  server.closeAllConnections();
+  await new Promise<void>((resolve) => server.close(() => resolve()));
+  process.removeListener('unhandledRejection', onUnhandled);
+  for (const l of SAVED_LISTENERS) process.on('unhandledRejection', l as (...a: any[]) => void);
+});
+beforeEach(() => {
+  h.toThrow = undefined;
+  h.logged.length = 0;
+  h.unhandled = 0;
+});
+
+const LINES = () => h.logged.filter((c) => c[0] === 'connector-token exchange failed');
+
+async function exchange(): Promise<{ status: number; code: string | undefined; minted: boolean } | null> {
+  try {
+    const res = await realFetch(baseUrl + '/internal/connector-token', {
+      method: 'POST',
+      headers: { 'Content-Type': 'application/json' },
+      body: JSON.stringify({ apiKey: 'sk_ks1868_connector_key_000' }),
+      signal: AbortSignal.timeout(1500),
+    });
+    const text = await res.text();
+    let code: string | undefined;
+    try {
+      code = JSON.parse(text)?.error?.code;
+    } catch {
+      code = undefined;
+    }
+    return { status: res.status, code, minted: text.includes('MINTED_1868_CONNECTOR') };
+  } catch {
+    return null;
+  }
+}
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
+/** The logged `error` field as a string; the type name when it is not one (a hostile value never reaches an assertion). */
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
+const BAD_GATEWAY = { status: 502, code: 'BAD_GATEWAY', minted: false };
+
+describe('KS-1868 the connector-token catch logs text for a hostile non-string message', () => {
+  it('control ks1868 C1: an ordinary Error is logged with its message and the route answers 502 BAD_GATEWAY with no token', async () => {
+    h.toThrow = new Error('security down');
+    expect(await exchange()).toEqual(BAD_GATEWAY);
+    expect(h.unhandled).toBe(0);
+    expect(LINES()).toHaveLength(1);
+    expect(reasonOf(LINES()[0])).toBe('security down');
+  });
+
+  it('control ks1868 C2: a thrown undefined makes the message read throw and the constant reason is logged', async () => {
+    h.toThrow = undefined;
+    expect(await exchange()).toEqual(BAD_GATEWAY);
+    expect(h.unhandled).toBe(0);
+    expect(LINES()).toHaveLength(1);
+    expect(reasonOf(LINES()[0])).toBe('unreadable thrown value');
+  });
+
+  it('control ks1868 C3: a thrown plain string has no message and is logged with no error field (not the text undefined)', async () => {
+    h.toThrow = 'plain boom';
+    expect(await exchange()).toEqual(BAD_GATEWAY);
+    expect(h.unhandled).toBe(0);
+    expect(LINES()).toHaveLength(1);
+    expect(reasonOf(LINES()[0])).toBe('<undefined>');
+  });
+
+  it('RED ks1868 R1 : a rejection whose message is a revoked Proxy logs the constant reason and the route answers 502 with no token', async () => {
+    h.toThrow = withMessage(SHAPES[0][1]());
+    expect(await exchange()).toEqual(BAD_GATEWAY);
+    expect(h.unhandled).toBe(0);
+    expect(LINES()).toHaveLength(1);
+    expect(reasonOf(LINES()[0])).toBe(SHAPES[0][2]);
+  });
+
+  it('RED ks1868 R2 : a rejection whose message is an object whose toString throws logs the constant reason and the route answers 502 with no token', async () => {
+    h.toThrow = withMessage(SHAPES[1][1]());
+    expect(await exchange()).toEqual(BAD_GATEWAY);
+    expect(h.unhandled).toBe(0);
+    expect(LINES()).toHaveLength(1);
+    expect(reasonOf(LINES()[0])).toBe(SHAPES[1][2]);
+  });
+
+  it('RED ks1868 R3 : a rejection whose message is a null-prototype object logs the constant reason and the route answers 502 with no token', async () => {
+    h.toThrow = withMessage(SHAPES[2][1]());
+    expect(await exchange()).toEqual(BAD_GATEWAY);
+    expect(h.unhandled).toBe(0);
+    expect(LINES()).toHaveLength(1);
+    expect(reasonOf(LINES()[0])).toBe(SHAPES[2][2]);
+  });
+
+  it('RED ks1868 R4 : a rejection whose message is a Symbol logs the Symbol text and the route answers 502 with no token', async () => {
+    h.toThrow = withMessage(SHAPES[3][1]());
+    expect(await exchange()).toEqual(BAD_GATEWAY);
+    expect(h.unhandled).toBe(0);
+    expect(LINES()).toHaveLength(1);
+    expect(reasonOf(LINES()[0])).toBe(SHAPES[3][2]);
+  });
+});
```
