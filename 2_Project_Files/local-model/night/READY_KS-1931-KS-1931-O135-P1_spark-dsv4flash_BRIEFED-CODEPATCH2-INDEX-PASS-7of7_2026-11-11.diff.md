# READY — KS-1931-KS-1931-O135-P1 (Spark (DeepSeek V4 Flash), briefed, code_patch2, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-11_ks_1931_o135_p1_kyc_erasure_cascade_stops_when_the_verification_read_fails/out.md.checker/patch.diff`** (from `ls` at 14:37 2026-11-11; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-11_ks_1931_o135_p1_kyc_erasure_cascade_stops_when_the_verification_read_fails/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-11_ks_1931_o135_p1_kyc_erasure_cascade_stops_when_the_verification_read_fails/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-11_ks_1931_o135_p1_kyc_erasure_cascade_stops_when_the_verification_read_fails/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-11_ks_1931_o135_p1_kyc_erasure_cascade_stops_when_the_verification_read_fails-control-r2/out.md.checker/patch.diff` rc 0, Spark operator o135 (Wednesday)).

**Held 14:37 2026-11-11 by Spark operator o135 (Wednesday) after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-11_ks_1931_o135_p1_kyc_erasure_cascade_stops_when_the_verification_read_fails/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `4a91ff3e1c56326da501f352ae2e9b2e3308fa4e`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/services/kyc/src/index.ts } + { Blockchain/Dev/services/kyc/src/__tests__/ks1931-erasure-cascade-stops-when-the-verification-read-fails.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/kyc/src/index.ts` (product) and `Blockchain/Dev/services/kyc/src/__tests__/ks1931-erasure-cascade-stops-when-the-verification-read-fails.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
4	2	Blockchain/Dev/services/kyc/src/index.ts
151	0	Blockchain/Dev/services/kyc/src/__tests__/ks1931-erasure-cascade-stops-when-the-verification-read-fails.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (4 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: index.ts`
- CODE_PATCH2 (rung 3, 1 product files + 1 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/services/kyc/src/index.ts`; test(s): `Blockchain/Dev/services/kyc/src/__tests__/ks1931-erasure-cascade-stops-when-the-verification-read-fails.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/services/kyc/src/index.ts 4 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/kyc/src/__tests__/ks1931-erasure-cascade-stops-when-the-verification-read-fails.test.ts 151 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/kyc/src/index.ts` (hunks=3, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/kyc/src/__tests__/ks1931-erasure-cascade-stops-when-the-verification-read-fails.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (2 failed / 4 run; controls green; assertion reds)` [red_first.json: failed=2 of total=4; red cell(s): ['KS-1931 the erasure cascade stops when the verification read fails RED ks1931 R1 an ordinary Error on the verification read stops the erasure before any DELETE and never answers 200', 'KS-1931 the erasure cascade stops when the verification read fails RED ks1931 R2 an unreadable thrown value on the verification read stops the erasure before any DELETE and never answers 200']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 1 product section(s) (4 passed / 4 run)` [green_after.json: failed=0 of total=4, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=90 failed=0 | after: total=94 failed=0` · `NEW reds: []` [baseline_suite.json total=90 failed=0; after_suite.json total=94 failed=0]
- A6 [verbatim]: `PASS A6 whole services/kyc suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/kyc: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 products=1 tests=1 red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/kyc/src/index.ts` (+4/-2 per numstat.out) and the test file `Blockchain/Dev/services/kyc/src/__tests__/ks1931-erasure-cascade-stops-when-the-verification-read-fails.test.ts` (+151/-0); 2 files in all (code_patch2: products Blockchain/Dev/services/kyc/src/index.ts). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `4a91ff3e1c56326da501f352ae2e9b2e3308fa4e` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-11_ks_1931_o135_p1_kyc_erasure_cascade_stops_when_the_verification_read_fails/input.json`. brief NOT LOCATED under night/briefs/ (no claim made). Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-11_ks_1931_o135_p1_kyc_erasure_cascade_stops_when_the_verification_read_fails/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/kyc/src/index.ts b/Blockchain/Dev/services/kyc/src/index.ts
--- a/Blockchain/Dev/services/kyc/src/index.ts
+++ b/Blockchain/Dev/services/kyc/src/index.ts
@@ -223,4 +223,4 @@
-async function dbGetVerificationsByUser(userId: string): Promise<KYCVerification[]> {
+async function dbGetVerificationsByUser(userId: string, throwOnError = false): Promise<KYCVerification[]> {
   if (!isDbAvailable()) return [];
   try {
     const result = await query(
@@ -237,6 +237,8 @@
       reason = 'unreadable thrown value';
     }
     logger.error('DB get verifications by user failed', { userId, error: reason });
+    // KS-1931: the erasure cascade passes throwOnError so a failed read stops it (its own comment: failures THROW); every other caller keeps the empty list.
+    if (throwOnError) throw err;
     return [];
   }
 }
@@ -387,7 +389,7 @@
   // destroyed) — in that case the user_id-column path below still applies to
   // post-035 images, and unreadable-blob legacy images are handled by the
   // 035 backfill having stamped user_id on them.
-  const verifications = await dbGetVerificationsByUser(userId);
+  const verifications = await dbGetVerificationsByUser(userId, true);
   const imageIds = new Set<string>();
   for (const v of verifications) {
     for (const d of v.documents || []) {
diff --git a/Blockchain/Dev/services/kyc/src/__tests__/ks1931-erasure-cascade-stops-when-the-verification-read-fails.test.ts b/Blockchain/Dev/services/kyc/src/__tests__/ks1931-erasure-cascade-stops-when-the-verification-read-fails.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/kyc/src/__tests__/ks1931-erasure-cascade-stops-when-the-verification-read-fails.test.ts
@@ -0,0 +1,151 @@
+import { describe, it, expect, vi, beforeAll, beforeEach, afterAll } from 'vitest';
+import http from 'http';
+import { randomUUID } from 'crypto';
+
+process.env.KYC_PROVIDER = 'mock';
+process.env.NODE_ENV = 'test';
+
+// KS-1931: dbDeleteUserData (the GDPR erasure cascade) read the user's verifications through dbGetVerificationsByUser, which logs a failed
+// read and returns [], so the cascade went on with an empty image list and deleted the verification rows by user_id: the legacy images only
+// those rows pointed to survived, and the route answered that all data was deleted. Its own comment says failures THROW. The cascade now
+// asks for the throwing form; GET /api/kyc/user/:userId keeps the empty list. Harness: the ks1868 one (real app on a real listener, the
+// db and subject-DEK modules replaced). The route has no try block, so a failed cascade leaves the request unanswered: the cells give the
+// request a short deadline and count the unhandled rejection themselves.
+const h = vi.hoisted(() => ({
+  toThrow: undefined as unknown,
+  failOn: undefined as RegExp | undefined,
+  sqls: [] as string[],
+  unhandled: 0,
+}));
+
+vi.mock('../db', () => ({
+  initDb: async () => undefined,
+  isDbAvailable: () => true,
+  query: (sql: string) => {
+    h.sqls.push(String(sql));
+    if (h.failOn && h.failOn.test(String(sql))) return Promise.reject(h.toThrow);
+    return Promise.resolve({ rows: [] });
+  },
+}));
+
+vi.mock('../subjectDeks', () => ({
+  subjectDeks: {
+    getOrCreateDek: async () => Buffer.alloc(32, 7),
+    getDek: async () => Buffer.alloc(32, 7),
+    evict: () => undefined,
+  },
+}));
+
+vi.mock('../utils/logger', () => {
+  const noop = () => undefined;
+  const logger = { info: noop, warn: noop, debug: noop, error: noop };
+  return { logger, createLogger: () => logger, validateEnv: () => undefined };
+});
+
+vi.mock('@secuura/shared', async (importOriginal) => {
+  const actual = await importOriginal<Record<string, unknown>>();
+  return {
+    ...actual,
+    encryptFieldWithDek: (plain: string) => plain,
+    isEncryptedPii: () => false,
+    isSubjectDekCiphertext: () => false,
+    authenticate: () => (_req: unknown, _res: unknown, next: () => void) => next(),
+  };
+});
+
+vi.mock('express', async (importOriginal) => {
+  const actual: any = (await importOriginal<any>()).default ?? (await importOriginal<any>());
+  const factory: any = (...args: any[]) => {
+    const app = actual(...args);
+    app.listen = () => ({ close: (cb?: () => void) => cb?.(), address: () => ({ port: 0 }), on() { return this; } });
+    return app;
+  };
+  Object.assign(factory, actual);
+  return { ...actual, default: factory };
+});
+
+const TIMEOUT_MS = 2500;
+const USER_ID = randomUUID();
+const SAVED_LISTENERS = process.listeners('unhandledRejection');
+const onUnhandled = () => {
+  h.unhandled += 1;
+};
+
+let httpServer: http.Server;
+let origin: string;
+
+async function startApp() {
+  if (httpServer) return;
+  const app = (await import('../index')).default as any;
+  httpServer = http.createServer(app);
+  await new Promise<void>((resolve) => httpServer.listen(0, '127.0.0.1', () => resolve()));
+  origin = 'http://127.0.0.1:' + String((httpServer.address() as any).port);
+}
+
+/** undefined when the request got no answer inside the deadline. */
+async function callRoute(method: string, path: string) {
+  const res = await fetch(origin + path, { method, signal: AbortSignal.timeout(TIMEOUT_MS) }).catch(() => undefined);
+  if (!res) return undefined;
+  const parsed: any = await res.json().catch(() => undefined);
+  return { status: res.status, body: parsed };
+}
+
+const erase = () => callRoute('DELETE', '/api/kyc/user/' + USER_ID + '/data');
+const read = () => callRoute('GET', '/api/kyc/user/' + USER_ID);
+const DELETES = () => h.sqls.filter((s) => /^\s*DELETE/i.test(s));
+
+afterAll(async () => {
+  if (httpServer) {
+    (httpServer as http.Server & { closeAllConnections?: () => void }).closeAllConnections?.();
+    await new Promise<void>((resolve) => httpServer.close(() => resolve()));
+  }
+  process.removeListener('unhandledRejection', onUnhandled);
+  for (const l of SAVED_LISTENERS) process.on('unhandledRejection', l as (...a: any[]) => void);
+});
+
+describe('KS-1931 the erasure cascade stops when the verification read fails', () => {
+  beforeAll(async () => {
+    process.removeAllListeners('unhandledRejection');
+    process.on('unhandledRejection', onUnhandled);
+    await startApp();
+  }, 120_000);
+
+  beforeEach(() => {
+    h.toThrow = undefined;
+    h.failOn = undefined;
+    h.sqls.length = 0;
+    h.unhandled = 0;
+  });
+
+  it('control ks1931 C1 with the read working, the erasure answers 200 and runs its three DELETE statements', async () => {
+    const res = await erase();
+    expect(res?.status).toBe(200);
+    expect(DELETES()).toHaveLength(3);
+  });
+
+  it('control ks1931 C2 an ordinary read failure still lets GET /api/kyc/user/:userId answer an empty list', async () => {
+    h.failOn = /SELECT \* FROM svc_kyc_verifications WHERE user_id/;
+    h.toThrow = new Error('db down');
+    const res = await read();
+    expect(res?.status).toBe(200);
+    expect(res?.body?.data?.count).toBe(0);
+  });
+
+  it('RED ks1931 R1 an ordinary Error on the verification read stops the erasure before any DELETE and never answers 200', async () => {
+    h.failOn = /SELECT \* FROM svc_kyc_verifications WHERE user_id/;
+    h.toThrow = new Error('db down');
+    const res = await erase();
+    expect(DELETES()).toHaveLength(0);
+    expect(res?.status).not.toBe(200);
+  });
+
+  it('RED ks1931 R2 an unreadable thrown value on the verification read stops the erasure before any DELETE and never answers 200', async () => {
+    const { proxy, revoke } = Proxy.revocable({}, {});
+    revoke();
+    h.failOn = /SELECT \* FROM svc_kyc_verifications WHERE user_id/;
+    h.toThrow = proxy;
+    const res = await erase();
+    expect(DELETES()).toHaveLength(0);
+    expect(res?.status).not.toBe(200);
+  });
+});
```
