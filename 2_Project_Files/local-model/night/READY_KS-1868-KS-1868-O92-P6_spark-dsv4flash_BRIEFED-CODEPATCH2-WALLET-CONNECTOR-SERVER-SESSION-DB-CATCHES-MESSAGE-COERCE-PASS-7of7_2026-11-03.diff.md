# READY — KS-1868-KS-1868-O92-P6 (spark-dsv4flash, briefed, code_patch2, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o92_p6_wallet_connector_server_session_save_get_disconnect_list_db_catches_guard_message/out.md.checker/patch.diff`** (from `ls` at 08:51 2026-11-03; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o92_p6_wallet_connector_server_session_save_get_disconnect_list_db_catches_guard_message/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o92_p6_wallet_connector_server_session_save_get_disconnect_list_db_catches_guard_message/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o92_p6_wallet_connector_server_session_save_get_disconnect_list_db_catches_guard_message/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o92_p6_wallet_connector_server_session_save_get_disconnect_list_db_catches_guard_message-control/out.md.checker/patch.diff` rc 0, Wednesday).

**Held 08:51 2026-11-03 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o92_p6_wallet_connector_server_session_save_get_disconnect_list_db_catches_guard_message/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `b85b7b6786fa6329b6f781cebf2475147738004e`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/services/wallet-connector/src/server.ts } + { Blockchain/Dev/services/wallet-connector/src/__tests__/ks1868-wallet-connector-server-session-db-catches-unreadable-throw.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/wallet-connector/src/server.ts` (product) and `Blockchain/Dev/services/wallet-connector/src/__tests__/ks1868-wallet-connector-server-session-db-catches-unreadable-throw.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
32	4	Blockchain/Dev/services/wallet-connector/src/server.ts
165	0	Blockchain/Dev/services/wallet-connector/src/__tests__/ks1868-wallet-connector-server-session-db-catches-unreadable-throw.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (32 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: server.ts`
- CODE_PATCH2 (rung 3, 1 product files + 1 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/services/wallet-connector/src/server.ts`; test(s): `Blockchain/Dev/services/wallet-connector/src/__tests__/ks1868-wallet-connector-server-session-db-catches-unreadable-throw.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/services/wallet-connector/src/server.ts 32 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/wallet-connector/src/__tests__/ks1868-wallet-connector-server-session-db-catches-unreadable-throw.test.ts 165 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/wallet-connector/src/server.ts` (hunks=4, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/wallet-connector/src/__tests__/ks1868-wallet-connector-server-session-db-catches-unreadable-throw.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (8 failed / 12 run; controls green; assertion reds)` [red_first.json: failed=8 of total=12; red cell(s): ['KS-1868 the wallet-connector DB catches answer as usual and log text for a hostile thrown value RED ks1868 R1: a revoked Proxy on POST /api/wallets/session is logged as text and the route answers 201', 'KS-1868 the wallet-connector DB catches answer as usual and log text for a hostile thrown value RED ks1868 R2: an Error whose message getter throws on POST /api/wallets/session is logged as text and the route answers 201', 'KS-1868 the wallet-connector DB catches answer as usual and log text for a hostile thrown value RED ks1868 R3: a revoked Proxy on GET /api/wallets/session/:sessionId is logged as text and the route answers 404', 'KS-1868 the wallet-connector DB catches answer as usual and log text for a hostile thrown value RED ks1868 R4: an Error whose message getter throws on GET /api/wallets/session/:sessionId is logged as text and the route answers 404', 'KS-1868 the wallet-connector DB catches answer as usual and log text for a hostile thrown value RED ks1868 R5: a revoked Proxy on DELETE /api/wallets/session/:sessionId is logged as text and the route answers 404', 'KS-1868 the wallet-connector DB catches answer as usual and log text for a hostile thrown value RED ks1868 R6: an Error whose message getter throws on DELETE /api/wallets/session/:sessionId is logged as text and the route answers 404', 'KS-1868 the wallet-connector DB catches answer as usual and log text for a hostile thrown value RED ks1868 R7: a revoked Proxy on GET /api/wallets/sessions is logged as text and the route answers 200', 'KS-1868 the wallet-connector DB catches answer as usual and log text for a hostile thrown value RED ks1868 R8: an Error whose message getter throws on GET /api/wallets/sessions is logged as text and the route answers 200']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 1 product section(s) (12 passed / 12 run)` [green_after.json: failed=0 of total=12, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=76 failed=1 | after: total=88 failed=0` · `NEW reds: []` [baseline_suite.json total=76 failed=1; after_suite.json total=88 failed=0]
- A6 [verbatim]: `PASS A6 whole services/wallet-connector suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/wallet-connector: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 products=1 tests=1 red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/wallet-connector/src/server.ts` (+32/-4 per numstat.out) and the test file `Blockchain/Dev/services/wallet-connector/src/__tests__/ks1868-wallet-connector-server-session-db-catches-unreadable-throw.test.ts` (+165/-0); 2 files in all (code_patch2: products Blockchain/Dev/services/wallet-connector/src/server.ts). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `b85b7b6786fa6329b6f781cebf2475147738004e` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o92_p6_wallet_connector_server_session_save_get_disconnect_list_db_catches_guard_message/input.json`. Brief (given by --brief; its `# ` heading names KS-1868): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1868_o92_p6_wallet_connector_server_session_save_get_disconnect_list_db_catches_guard_message/KS-1868.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o92_p6_wallet_connector_server_session_save_get_disconnect_list_db_catches_guard_message/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/wallet-connector/src/server.ts b/Blockchain/Dev/services/wallet-connector/src/server.ts
--- a/Blockchain/Dev/services/wallet-connector/src/server.ts
+++ b/Blockchain/Dev/services/wallet-connector/src/server.ts
@@ -64,6 +64,13 @@
       [s.sessionId, s.walletType, s.address, s.connected, s.connectedAt]
     );
   } catch (err: any) {
-    logger.error('DB save session failed', { error: err?.message });
+    let reason: string | null | undefined;
+    try {
+      const m = err?.message;
+      reason = m === undefined || m === null ? m : String(m);
+    } catch {
+      reason = 'unreadable thrown value';
+    }
+    logger.error('DB save session failed', { error: reason });
   }
 }
@@ -186,6 +193,13 @@
         memConnectedWallets.set(sessionId, session);
       }
     } catch (err: any) {
-      logger.error('DB get session failed', { error: err?.message });
+      let reason: string | null | undefined;
+      try {
+        const m = err?.message;
+        reason = m === undefined || m === null ? m : String(m);
+      } catch {
+        reason = 'unreadable thrown value';
+      }
+      logger.error('DB get session failed', { error: reason });
     }
   }
@@ -214,6 +228,13 @@
     try {
       await query('UPDATE svc_wallet_sessions SET connected = false WHERE id = $1', [sessionId]);
     } catch (err: any) {
-      logger.error('DB disconnect session failed', { error: err?.message });
+      let reason: string | null | undefined;
+      try {
+        const m = err?.message;
+        reason = m === undefined || m === null ? m : String(m);
+      } catch {
+        reason = 'unreadable thrown value';
+      }
+      logger.error('DB disconnect session failed', { error: reason });
     }
   }
@@ -298,6 +319,13 @@
         memConnectedWallets.set(row.id, session);
       }
     } catch (err: any) {
-      logger.error('DB list sessions failed', { error: err?.message });
+      let reason: string | null | undefined;
+      try {
+        const m = err?.message;
+        reason = m === undefined || m === null ? m : String(m);
+      } catch {
+        reason = 'unreadable thrown value';
+      }
+      logger.error('DB list sessions failed', { error: reason });
     }
   }
diff --git a/Blockchain/Dev/services/wallet-connector/src/__tests__/ks1868-wallet-connector-server-session-db-catches-unreadable-throw.test.ts b/Blockchain/Dev/services/wallet-connector/src/__tests__/ks1868-wallet-connector-server-session-db-catches-unreadable-throw.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/wallet-connector/src/__tests__/ks1868-wallet-connector-server-session-db-catches-unreadable-throw.test.ts
@@ -0,0 +1,165 @@
+import { describe, it, expect, beforeAll, afterAll, beforeEach, afterEach, vi } from 'vitest';
+import http from 'http';
+import type { AddressInfo } from 'net';
+import type { RequestHandler } from 'express';
+
+// KS-1868 (operator 92 screen, wallet-connector server): four DB catches of services/wallet-connector/src/server.ts pass `err?.message` straight into the
+// logger's meta object, unguarded: dbSaveWalletSession (line 67, POST /api/wallets/session), the database read of GET /api/wallets/session/:sessionId
+// (line 189), the disconnect update of DELETE /api/wallets/session/:sessionId (line 217) and the database read of GET /api/wallets/sessions (line 301).
+// `?.` guards null and undefined only: a thrown value whose read throws (a revoked Proxy, an Error whose message getter throws) makes the catch throw, so the
+// async handler rejects (an unhandled rejection) and the request never gets its answer where an ordinary Error is logged and the route answers as usual
+// (201; 404 NOT_FOUND; 404 NOT_FOUND; 200). The cells make every database statement reject with such a value and assert the usual answer, no unhandled
+// rejection and a logged line that carries text. Harness: the real server.ts app on 127.0.0.1; server.ts boots at import, so the boot is held off (initDb never
+// settles, the user.erased subscriber is a no-op), the database stand-in reads as available and rejects every statement with the value, the shared JWT
+// check is a stand-in that sets a platform administrator, and the logger is a plain recording object (no database, no network).
+const h = vi.hoisted(() => ({
+  toThrow: undefined as unknown,
+  logs: [] as { level: string; message: string; meta: Record<string, unknown> | undefined }[],
+  unhandled: 0,
+}));
+
+vi.mock('../db', () => ({
+  initDb: () => new Promise<boolean>(() => {}),
+  isDbAvailable: () => true,
+  query: (..._args: unknown[]) => Promise.reject(h.toThrow),
+}));
+vi.mock('../userErasedSubscriber', () => ({
+  startUserErasedSubscriber: async () => {},
+}));
+vi.mock('../utils/logger', () => {
+  const rec = (level: string) => (message: string, meta?: Record<string, unknown>) => {
+    h.logs.push({ level, message, meta });
+  };
+  return { logger: { debug: rec('debug'), info: rec('info'), warn: rec('warn'), error: rec('error') } };
+});
+vi.mock('@secuura/shared', async (importOriginal) => ({
+  ...(await importOriginal<Record<string, unknown>>()),
+  authenticate: () =>
+    ((req, _res, next) => {
+      (req as unknown as { user: unknown }).user = { userId: '00000000-0000-4000-8000-000000000001', role: 'SYSTEM_ADMIN' };
+      next();
+    }) as RequestHandler,
+}));
+
+import app from '../server';
+
+let base = '';
+let server: http.Server;
+const SAVED_LISTENERS = process.listeners('unhandledRejection');
+const onUnhandled = () => {
+  h.unhandled += 1;
+};
+
+beforeAll(async () => {
+  server = http.createServer(app);
+  await new Promise<void>((resolve) => server.listen(0, '127.0.0.1', () => resolve()));
+  base = 'http://127.0.0.1:' + (server.address() as AddressInfo).port;
+});
+afterAll(async () => {
+  await new Promise<void>((resolve) => server?.close(() => resolve()));
+});
+beforeEach(() => {
+  h.toThrow = undefined;
+  h.logs.length = 0;
+  h.unhandled = 0;
+  process.removeAllListeners('unhandledRejection');
+  process.on('unhandledRejection', onUnhandled);
+});
+afterEach(() => {
+  process.removeListener('unhandledRejection', onUnhandled);
+  for (const l of SAVED_LISTENERS) process.on('unhandledRejection', l as (...a: any[]) => void);
+});
+
+/** The answer as {status, code}; null when the request got none within the deadline (a hang). */
+async function call(method: string, path: string, body?: object): Promise<{ status: number; code: string | undefined } | null> {
+  try {
+    const r = await fetch(base + path, {
+      method,
+      headers: body ? { 'content-type': 'application/json' } : {},
+      body: body ? JSON.stringify(body) : undefined,
+      signal: AbortSignal.timeout(1500),
+    });
+    const payload = (await r.json()) as { error?: { code?: string } };
+    return { status: r.status, code: payload.error?.code };
+  } catch {
+    return null;
+  }
+}
+
+const LINES = (message: string) => h.logs.filter((l) => l.message === message);
+/** The logged `error` field as a string; the type name when it is not one (a hostile value never reaches an assertion). */
+const reasonOf = (l: { meta: Record<string, unknown> | undefined } | undefined): string => {
+  const v = l?.meta?.error;
+  return typeof v === 'string' ? v : '<' + typeof v + '>';
+};
+
+const revokedProxy = (): unknown => {
+  const rp = Proxy.revocable({}, {});
+  rp.revoke();
+  return rp.proxy;
+};
+const getterThrows = (): unknown =>
+  Object.create(Error.prototype, {
+    message: {
+      get() {
+        throw new Error('getter boom');
+      },
+    },
+  });
+
+const SITES = [
+  { name: 'POST /api/wallets/session (dbSaveWalletSession)', log: 'DB save session failed', method: 'POST', path: '/api/wallets/session', body: { walletType: 'nami', address: 'addr_ks1868' }, answer: { status: 201, code: undefined } },
+  { name: 'GET /api/wallets/session/:sessionId', log: 'DB get session failed', method: 'GET', path: '/api/wallets/session/ks1868-unknown', body: undefined, answer: { status: 404, code: 'NOT_FOUND' } },
+  { name: 'DELETE /api/wallets/session/:sessionId', log: 'DB disconnect session failed', method: 'DELETE', path: '/api/wallets/session/ks1868-unknown', body: undefined, answer: { status: 404, code: 'NOT_FOUND' } },
+  { name: 'GET /api/wallets/sessions', log: 'DB list sessions failed', method: 'GET', path: '/api/wallets/sessions', body: undefined, answer: { status: 200, code: undefined } },
+];
+
+async function run(s: (typeof SITES)[number], value: unknown, reason: string): Promise<void> {
+  h.toThrow = value;
+  const got = await call(s.method, s.path, s.body);
+  await new Promise<void>((resolve) => setTimeout(resolve, 25));
+  expect(got).toEqual(s.answer);
+  expect(h.unhandled).toBe(0);
+  expect(LINES(s.log)).toHaveLength(1);
+  expect(reasonOf(LINES(s.log)[0])).toBe(reason);
+}
+const CONSTANT = 'unreadable thrown value';
+
+describe('KS-1868 the wallet-connector DB catches answer as usual and log text for a hostile thrown value', () => {
+  it('control ks1868 C1: an ordinary Error on POST /api/wallets/session is logged with its message and the route answers 201', async () => {
+    await run(SITES[0], new Error('db boom'), 'db boom');
+  });
+  it('control ks1868 C2: an ordinary Error on GET /api/wallets/session/:sessionId is logged with its message and the route answers 404', async () => {
+    await run(SITES[1], new Error('db boom'), 'db boom');
+  });
+  it('control ks1868 C3: an ordinary Error on DELETE /api/wallets/session/:sessionId is logged with its message and the route answers 404', async () => {
+    await run(SITES[2], new Error('db boom'), 'db boom');
+  });
+  it('control ks1868 C4: an ordinary Error on GET /api/wallets/sessions is logged with its message and the route answers 200', async () => {
+    await run(SITES[3], new Error('db boom'), 'db boom');
+  });
+  it('RED ks1868 R1: a revoked Proxy on POST /api/wallets/session is logged as text and the route answers 201', async () => {
+    await run(SITES[0], revokedProxy(), CONSTANT);
+  });
+  it('RED ks1868 R2: an Error whose message getter throws on POST /api/wallets/session is logged as text and the route answers 201', async () => {
+    await run(SITES[0], getterThrows(), CONSTANT);
+  });
+  it('RED ks1868 R3: a revoked Proxy on GET /api/wallets/session/:sessionId is logged as text and the route answers 404', async () => {
+    await run(SITES[1], revokedProxy(), CONSTANT);
+  });
+  it('RED ks1868 R4: an Error whose message getter throws on GET /api/wallets/session/:sessionId is logged as text and the route answers 404', async () => {
+    await run(SITES[1], getterThrows(), CONSTANT);
+  });
+  it('RED ks1868 R5: a revoked Proxy on DELETE /api/wallets/session/:sessionId is logged as text and the route answers 404', async () => {
+    await run(SITES[2], revokedProxy(), CONSTANT);
+  });
+  it('RED ks1868 R6: an Error whose message getter throws on DELETE /api/wallets/session/:sessionId is logged as text and the route answers 404', async () => {
+    await run(SITES[2], getterThrows(), CONSTANT);
+  });
+  it('RED ks1868 R7: a revoked Proxy on GET /api/wallets/sessions is logged as text and the route answers 200', async () => {
+    await run(SITES[3], revokedProxy(), CONSTANT);
+  });
+  it('RED ks1868 R8: an Error whose message getter throws on GET /api/wallets/sessions is logged as text and the route answers 200', async () => {
+    await run(SITES[3], getterThrows(), CONSTANT);
+  });
+});
```
