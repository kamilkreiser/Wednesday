# READY — KS-1868-KS-1868-O75-P2 (spark-dsv4flash, briefed, code_patch2, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o75_p2_anchoring_read_route_catches_unreadable_throw/out.md.checker/patch.diff`** (from `ls` at 13:38 2026-11-02; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o75_p2_anchoring_read_route_catches_unreadable_throw/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o75_p2_anchoring_read_route_catches_unreadable_throw/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o75_p2_anchoring_read_route_catches_unreadable_throw/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o75_p2_anchoring_read_route_catches_unreadable_throw-control/out.md.checker/patch.diff` rc 0, Wednesday).

**Held 13:38 2026-11-02 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o75_p2_anchoring_read_route_catches_unreadable_throw/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `04ff5262ad526a13c1a0df99480b76860a8d11d1`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/services/anchoring/src/index.ts } + { Blockchain/Dev/services/anchoring/src/__tests__/ks1868-anchoring-read-route-catches-unreadable-throw.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/anchoring/src/index.ts` (product) and `Blockchain/Dev/services/anchoring/src/__tests__/ks1868-anchoring-read-route-catches-unreadable-throw.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
21	3	Blockchain/Dev/services/anchoring/src/index.ts
241	0	Blockchain/Dev/services/anchoring/src/__tests__/ks1868-anchoring-read-route-catches-unreadable-throw.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (21 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: index.ts`
- CODE_PATCH2 (rung 3, 1 product files + 1 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/services/anchoring/src/index.ts`; test(s): `Blockchain/Dev/services/anchoring/src/__tests__/ks1868-anchoring-read-route-catches-unreadable-throw.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/services/anchoring/src/index.ts 21 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/anchoring/src/__tests__/ks1868-anchoring-read-route-catches-unreadable-throw.test.ts 241 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/anchoring/src/index.ts` (hunks=3, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/anchoring/src/__tests__/ks1868-anchoring-read-route-catches-unreadable-throw.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (6 failed / 9 run; controls green; assertion reds)` [red_first.json: failed=6 of total=9; red cell(s): ['KS-1868 the anchoring read-route catches read the rejection value safely RED ks1868 R1 tx lookup: a revoked Proxy rejection logs a constant reason and the route answers 404', 'KS-1868 the anchoring read-route catches read the rejection value safely RED ks1868 R2 tx lookup: an Error whose message getter throws logs a constant reason and the route answers 404', 'KS-1868 the anchoring read-route catches read the rejection value safely RED ks1868 R3 verify-by-hash: a revoked Proxy rejection logs a constant reason and the chain step answers 404', 'KS-1868 the anchoring read-route catches read the rejection value safely RED ks1868 R4 verify-by-hash: an Error whose message getter throws logs a constant reason and the chain step answers 404', 'KS-1868 the anchoring read-route catches read the rejection value safely RED ks1868 R5 content-hash verify: a revoked Proxy rejection logs a constant reason and the route answers verified false', 'KS-1868 the anchoring read-route catches read the rejection value safely RED ks1868 R6 content-hash verify: an Error whose message getter throws logs a constant reason and the route answers verified false']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 1 product section(s) (9 passed / 9 run)` [green_after.json: failed=0 of total=9, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=751 failed=1 | after: total=760 failed=1` · `NEW reds: []` [baseline_suite.json total=751 failed=1; after_suite.json total=760 failed=1]
- A6 [verbatim]: `PASS A6 whole services/anchoring suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/anchoring: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 products=1 tests=1 red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/anchoring/src/index.ts` (+21/-3 per numstat.out) and the test file `Blockchain/Dev/services/anchoring/src/__tests__/ks1868-anchoring-read-route-catches-unreadable-throw.test.ts` (+241/-0); 2 files in all (code_patch2: products Blockchain/Dev/services/anchoring/src/index.ts). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `04ff5262ad526a13c1a0df99480b76860a8d11d1` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o75_p2_anchoring_read_route_catches_unreadable_throw/input.json`. Brief (given by --brief; its `# ` heading names KS-1868): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1868_o75_p2_anchoring_read_route_catches_unreadable_throw/KS-1868.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o75_p2_anchoring_read_route_catches_unreadable_throw/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/anchoring/src/index.ts b/Blockchain/Dev/services/anchoring/src/index.ts
--- a/Blockchain/Dev/services/anchoring/src/index.ts
+++ b/Blockchain/Dev/services/anchoring/src/index.ts
@@ -692,5 +692,11 @@
         return res.json(buildResponse('db', payload, row));
       }
     } catch (err: any) {
-      log('warn', 'verify-by-hash: local DB lookup failed', { error: err?.message });
+      let reason: string;
+      try {
+        reason = err?.message;
+      } catch {
+        reason = 'unreadable thrown value';
+      }
+      log('warn', 'verify-by-hash: local DB lookup failed', { error: reason });
     }
@@ -1302,5 +1308,11 @@
         }
       }
     } catch (err: any) {
-      log('warn', 'DB lookup anchor by content hash failed', { error: err?.message });
+      let reason: string;
+      try {
+        reason = err?.message;
+      } catch {
+        reason = 'unreadable thrown value';
+      }
+      log('warn', 'DB lookup anchor by content hash failed', { error: reason });
     }
@@ -1805,7 +1817,13 @@
     if (result.rows.length === 0) return undefined;
     return rowToAnchor(result.rows[0]);
   } catch (err: any) {
-    log('warn', 'DB lookup anchor by tx failed', { txHash, error: err?.message });
+    let reason: string;
+    try {
+      reason = err?.message;
+    } catch {
+      reason = 'unreadable thrown value';
+    }
+    log('warn', 'DB lookup anchor by tx failed', { txHash, error: reason });
     return undefined;
   }
 }
diff --git a/Blockchain/Dev/services/anchoring/src/__tests__/ks1868-anchoring-read-route-catches-unreadable-throw.test.ts b/Blockchain/Dev/services/anchoring/src/__tests__/ks1868-anchoring-read-route-catches-unreadable-throw.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/anchoring/src/__tests__/ks1868-anchoring-read-route-catches-unreadable-throw.test.ts
@@ -0,0 +1,241 @@
+// KS-1868: three read-side catches of the anchoring service log `error: err?.message` and carry on. When the rejection
+// value cannot be read (a revoked Proxy throws on property reads; an Error whose `message` getter throws, throws on
+// `.message`) the catch itself used to throw before its log line. Cells: GET /api/anchors/tx/:txHash
+// (`dbGetAnchorByTx` logs and returns undefined, the route answers 404), GET /api/anchors/verify/:hash (the local
+// anchor_store lookup logs and falls through to the chain step; with no Cardano credentials that is a 404) and
+// POST /api/anchors/verify (the content-hash lookup logs and the route answers verified:false). An ordinary Error is
+// the control on each route. Harness: the ks1822 suite (the real index.ts app served on an ephemeral port, a real
+// RS256 bearer, `../db` mocked). The query stand-in rejects with a plain function, not vi.fn(): a spy inspects what
+// it rejects with and could itself fail on a revoked Proxy before the code under test saw it. The cells count
+// unhandled rejections themselves and give the client a short timeout, so a hang shows as a failed assertion.
+// Nothing here submits, signs or writes an anchor: every statement the cells reject is a SELECT.
+import { describe, it, expect, beforeAll, afterAll, beforeEach, vi } from 'vitest';
+import crypto from 'crypto';
+import http from 'http';
+import type { AddressInfo } from 'net';
+import express from 'express';
+
+const h = vi.hoisted(() => ({
+  toThrow: undefined as unknown,
+  rejectPattern: null as RegExp | null,
+  writes: 0,
+  unhandled: 0,
+}));
+
+vi.mock('../db', async (importOriginal) => {
+  const real = await importOriginal<typeof import('../db')>();
+  return {
+    ...real,
+    isDbAvailable: () => true,
+    query: async (sql: string) => {
+      if (sql.includes('to_regclass')) return { rows: [{ s: 'anchor_store', b: 'anchor_batches' }], rowCount: 1 };
+      if (/^\s*(INSERT|UPDATE|DELETE|CREATE|ALTER)/i.test(sql)) h.writes += 1;
+      if (h.rejectPattern && h.rejectPattern.test(sql)) return Promise.reject(h.toThrow);
+      return { rows: [], rowCount: 0 };
+    },
+    transaction: async () => {
+      throw new Error('KS-1868 test: no transaction expected');
+    },
+  };
+});
+
+const TENANT_A = 'a1868000-0000-4000-8000-00000000000a';
+const ORG_A = 'c1868000-0000-4000-8000-0000000000ca';
+const TX = 'ab'.repeat(32);
+const HASH = 'cd'.repeat(32);
+const LOOKUP_DOWN = 'lookup down';
+const UNREADABLE = 'unreadable thrown value';
+
+const { privateKey, publicKey } = crypto.generateKeyPairSync('rsa', { modulusLength: 2048 });
+const PRIVATE_PEM = privateKey.export({ type: 'pkcs8', format: 'pem' }).toString();
+const PUBLIC_PEM = publicKey.export({ type: 'spki', format: 'pem' }).toString();
+const b64url = (b: Buffer): string => b.toString('base64').replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
+function bearer(): string {
+  const header = b64url(Buffer.from(JSON.stringify({ alg: 'RS256', typ: 'JWT' })));
+  const now = Math.floor(Date.now() / 1000);
+  const claims = { userId: '2a186800-0000-4000-8000-0000000018a2', role: 'user', organizationId: ORG_A, tenantId: TENANT_A };
+  const payload = b64url(Buffer.from(JSON.stringify({ iat: now, exp: now + 600, ...claims })));
+  return `${header}.${payload}.${b64url(crypto.sign('RSA-SHA256', Buffer.from(`${header}.${payload}`), PRIVATE_PEM))}`;
+}
+
+const SAVED_LISTENERS = process.listeners('unhandledRejection');
+const onUnhandled = () => {
+  h.unhandled += 1;
+};
+
+let server: http.Server;
+let base = '';
+const logLines: string[] = [];
+
+type Wire = { status: number; body: string } | null;
+async function send(method: 'GET' | 'POST', path: string, body?: unknown): Promise<Wire> {
+  try {
+    const res = await fetch(`${base}${path}`, {
+      method,
+      headers: { Authorization: `Bearer ${bearer()}`, 'Content-Type': 'application/json' },
+      body: body === undefined ? undefined : JSON.stringify(body),
+      signal: AbortSignal.timeout(1500),
+    });
+    return { status: res.status, body: await res.text() };
+  } catch {
+    return null;
+  }
+}
+/** index.ts `log()` writes one JSON object per console.log line; those whose `message` is `message`. */
+function lines(message: string): Array<Record<string, unknown>> {
+  return logLines
+    .filter((l) => l.startsWith('{') && l.includes(message))
+    .map((l) => JSON.parse(l) as Record<string, unknown>)
+    .filter((o) => o.message === message);
+}
+
+beforeAll(async () => {
+  process.removeAllListeners('unhandledRejection');
+  process.on('unhandledRejection', onUnhandled);
+  process.env.JWT_PUBLIC_KEY = Buffer.from(PUBLIC_PEM, 'utf8').toString('base64');
+  delete process.env.JWT_JWKS_URL;
+  delete process.env.AUTH_SERVICE_URL;
+  delete process.env.PLATFORM_WALLET_MNEMONIC;
+  delete process.env.BLOCKFROST_API_KEY;
+  delete process.env.DATABASE_URL;
+  process.env.CARDANO_NETWORK = 'preview';
+  vi.spyOn(console, 'log').mockImplementation((...args: unknown[]) => {
+    logLines.push(args.map(String).join(' '));
+  });
+  vi.spyOn(express.application, 'listen').mockReturnValue(
+    { keepAliveTimeout: 0, headersTimeout: 0, close: () => undefined } as unknown as http.Server,
+  );
+  const app = (await import('../index')).default;
+  server = http.createServer(app);
+  await new Promise<void>((resolve) => { server.listen(0, '127.0.0.1', resolve); });
+  base = `http://127.0.0.1:${(server.address() as AddressInfo).port}`;
+}, 60000);
+
+afterAll(async () => {
+  (server as any)?.closeAllConnections?.();
+  await new Promise<void>((resolve) => (server ? server.close(() => resolve()) : resolve()));
+  process.removeListener('unhandledRejection', onUnhandled);
+  for (const l of SAVED_LISTENERS) process.on('unhandledRejection', l as (...a: any[]) => void);
+  vi.restoreAllMocks();
+});
+
+beforeEach(() => {
+  h.toThrow = undefined;
+  h.rejectPattern = null;
+  h.writes = 0;
+  h.unhandled = 0;
+  logLines.length = 0;
+});
+
+const revokedProxy = (): unknown => {
+  const { proxy, revoke } = Proxy.revocable({}, {});
+  revoke();
+  return proxy;
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
+const TX_MSG = 'DB lookup anchor by tx failed';
+const HASH_MSG = 'verify-by-hash: local DB lookup failed';
+const VERIFY_MSG = 'DB lookup anchor by content hash failed';
+
+const byTx = () => {
+  h.rejectPattern = /WHERE transaction_hash = \$1/;
+  return send('GET', `/api/anchors/tx/${TX}`);
+};
+const byHash = () => {
+  h.rejectPattern = /LOWER\(content_hash\) = \$1/;
+  return send('GET', `/api/anchors/verify/${HASH}`);
+};
+const verify = () => {
+  h.rejectPattern = /content_hash = \$1 AND status = 'confirmed'/;
+  return send('POST', '/api/anchors/verify', { contentHash: HASH });
+};
+
+const TX_ANSWER = { success: false, error: { code: 'NOT_FOUND', message: 'Anchor not found for transaction' } };
+const HASH_ANSWER = { verified: false, hash: HASH, reason: 'Not found in local DB and Blockfrost not configured.' };
+const VERIFY_ANSWER = { success: true, data: { verified: false, reason: 'No confirmed anchor found for this hash', contentHash: HASH } };
+
+function expectAnswer(w: Wire, status: number, answer: unknown): void {
+  expect(w).not.toBeNull();
+  expect(w?.status, `received body: ${w?.body}`).toBe(status);
+  expect(JSON.parse(w?.body ?? 'null')).toEqual(answer);
+}
+
+describe('KS-1868 the anchoring read-route catches read the rejection value safely', () => {
+  it('control ks1868 C1 tx lookup: an ordinary Error is logged with its own message and the route answers 404', async () => {
+    h.toThrow = new Error(LOOKUP_DOWN);
+    expectAnswer(await byTx(), 404, TX_ANSWER);
+    expect(h.unhandled).toBe(0);
+    expect(lines(TX_MSG)).toHaveLength(1);
+    expect(lines(TX_MSG)[0]).toMatchObject({ level: 'warn', txHash: TX, error: LOOKUP_DOWN });
+    expect(h.writes).toBe(0);
+  });
+
+  it('control ks1868 C2 verify-by-hash: an ordinary Error is logged with its own message and the chain step answers 404', async () => {
+    h.toThrow = new Error(LOOKUP_DOWN);
+    expectAnswer(await byHash(), 404, HASH_ANSWER);
+    expect(lines(HASH_MSG)).toHaveLength(1);
+    expect(lines(HASH_MSG)[0]).toMatchObject({ level: 'warn', error: LOOKUP_DOWN });
+    expect(h.writes).toBe(0);
+  });
+
+  it('control ks1868 C3 content-hash verify: an ordinary Error is logged with its own message and the route answers verified false', async () => {
+    h.toThrow = new Error(LOOKUP_DOWN);
+    expectAnswer(await verify(), 200, VERIFY_ANSWER);
+    expect(lines(VERIFY_MSG)).toHaveLength(1);
+    expect(lines(VERIFY_MSG)[0]).toMatchObject({ level: 'warn', error: LOOKUP_DOWN });
+    expect(h.writes).toBe(0);
+  });
+
+  it('RED ks1868 R1 tx lookup: a revoked Proxy rejection logs a constant reason and the route answers 404', async () => {
+    h.toThrow = revokedProxy();
+    expectAnswer(await byTx(), 404, TX_ANSWER);
+    expect(h.unhandled).toBe(0);
+    expect(lines(TX_MSG)).toHaveLength(1);
+    expect(lines(TX_MSG)[0]).toMatchObject({ level: 'warn', txHash: TX, error: UNREADABLE });
+  });
+
+  it('RED ks1868 R2 tx lookup: an Error whose message getter throws logs a constant reason and the route answers 404', async () => {
+    h.toThrow = getterThrows();
+    expectAnswer(await byTx(), 404, TX_ANSWER);
+    expect(h.unhandled).toBe(0);
+    expect(lines(TX_MSG)).toHaveLength(1);
+    expect(lines(TX_MSG)[0]).toMatchObject({ level: 'warn', txHash: TX, error: UNREADABLE });
+  });
+
+  it('RED ks1868 R3 verify-by-hash: a revoked Proxy rejection logs a constant reason and the chain step answers 404', async () => {
+    h.toThrow = revokedProxy();
+    expectAnswer(await byHash(), 404, HASH_ANSWER);
+    expect(lines(HASH_MSG)).toHaveLength(1);
+    expect(lines(HASH_MSG)[0]).toMatchObject({ level: 'warn', error: UNREADABLE });
+  });
+
+  it('RED ks1868 R4 verify-by-hash: an Error whose message getter throws logs a constant reason and the chain step answers 404', async () => {
+    h.toThrow = getterThrows();
+    expectAnswer(await byHash(), 404, HASH_ANSWER);
+    expect(lines(HASH_MSG)).toHaveLength(1);
+    expect(lines(HASH_MSG)[0]).toMatchObject({ level: 'warn', error: UNREADABLE });
+  });
+
+  it('RED ks1868 R5 content-hash verify: a revoked Proxy rejection logs a constant reason and the route answers verified false', async () => {
+    h.toThrow = revokedProxy();
+    expectAnswer(await verify(), 200, VERIFY_ANSWER);
+    expect(lines(VERIFY_MSG)).toHaveLength(1);
+    expect(lines(VERIFY_MSG)[0]).toMatchObject({ level: 'warn', error: UNREADABLE });
+  });
+
+  it('RED ks1868 R6 content-hash verify: an Error whose message getter throws logs a constant reason and the route answers verified false', async () => {
+    h.toThrow = getterThrows();
+    expectAnswer(await verify(), 200, VERIFY_ANSWER);
+    expect(lines(VERIFY_MSG)).toHaveLength(1);
+    expect(lines(VERIFY_MSG)[0]).toMatchObject({ level: 'warn', error: UNREADABLE });
+    expect(h.writes).toBe(0);
+  });
+});
```
