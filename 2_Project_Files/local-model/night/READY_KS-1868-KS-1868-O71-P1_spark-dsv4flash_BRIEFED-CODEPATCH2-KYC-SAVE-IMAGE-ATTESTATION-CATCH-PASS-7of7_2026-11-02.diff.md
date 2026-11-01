# READY — KS-1868-KS-1868-O71-P1 (spark-dsv4flash, briefed, code_patch2, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o71_p1_kyc_save_image_attestation_catch_unreadable_throw/out.md.checker/patch.diff`** (from `ls` at 10:49 2026-11-02; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o71_p1_kyc_save_image_attestation_catch_unreadable_throw/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o71_p1_kyc_save_image_attestation_catch_unreadable_throw/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o71_p1_kyc_save_image_attestation_catch_unreadable_throw/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o71_p1_kyc_save_image_attestation_catch_unreadable_throw-control/out.md.checker/patch.diff` rc 0, Wednesday).

**Held 10:49 2026-11-02 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o71_p1_kyc_save_image_attestation_catch_unreadable_throw/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `bd8785796118a20b0220924523a543baf7f73340`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/services/kyc/src/index.ts } + { Blockchain/Dev/services/kyc/src/__tests__/ks1868-kyc-save-image-attestation-unreadable-throw.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/kyc/src/index.ts` (product) and `Blockchain/Dev/services/kyc/src/__tests__/ks1868-kyc-save-image-attestation-unreadable-throw.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
7	1	Blockchain/Dev/services/kyc/src/index.ts
215	0	Blockchain/Dev/services/kyc/src/__tests__/ks1868-kyc-save-image-attestation-unreadable-throw.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (7 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: index.ts`
- CODE_PATCH2 (rung 3, 1 product files + 1 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/services/kyc/src/index.ts`; test(s): `Blockchain/Dev/services/kyc/src/__tests__/ks1868-kyc-save-image-attestation-unreadable-throw.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/services/kyc/src/index.ts 7 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/kyc/src/__tests__/ks1868-kyc-save-image-attestation-unreadable-throw.test.ts 215 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/kyc/src/index.ts` (hunks=1, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/kyc/src/__tests__/ks1868-kyc-save-image-attestation-unreadable-throw.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (2 failed / 3 run; controls green; assertion reds)` [red_first.json: failed=2 of total=3; red cell(s): ['KS-1868 dbSaveImage reads the thrown value safely RED ks1868 R1 a revoked Proxy thrown value logs a constant reason and the upload is refused with the attestation failure', 'KS-1868 dbSaveImage reads the thrown value safely RED ks1868 R2 an Error whose message getter throws logs a constant reason and the upload is refused with the attestation failure']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 1 product section(s) (3 passed / 3 run)` [green_after.json: failed=0 of total=3, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=73 failed=0 | after: total=76 failed=0` · `NEW reds: []` [baseline_suite.json total=73 failed=0; after_suite.json total=76 failed=0]
- A6 [verbatim]: `PASS A6 whole services/kyc suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/kyc: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 products=1 tests=1 red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/kyc/src/index.ts` (+7/-1 per numstat.out) and the test file `Blockchain/Dev/services/kyc/src/__tests__/ks1868-kyc-save-image-attestation-unreadable-throw.test.ts` (+215/-0); 2 files in all (code_patch2: products Blockchain/Dev/services/kyc/src/index.ts). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `bd8785796118a20b0220924523a543baf7f73340` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o71_p1_kyc_save_image_attestation_catch_unreadable_throw/input.json`. Brief (given by --brief; its `# ` heading names KS-1868): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1868_o71_p1_kyc_save_image_attestation_catch_unreadable_throw/KS-1868.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o71_p1_kyc_save_image_attestation_catch_unreadable_throw/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/kyc/src/index.ts b/Blockchain/Dev/services/kyc/src/index.ts
--- a/Blockchain/Dev/services/kyc/src/index.ts
+++ b/Blockchain/Dev/services/kyc/src/index.ts
@@ -350,7 +350,13 @@
     // Deliberately NOT widened (Wednesday's ruling, 2026-09-06): no retry, no
     // queue, no schema check at boot. Failing loud IS the fix; anything more
     // is a separate ticket.
-    logger.error('DB save image failed', { error: err instanceof Error ? err.message : String(err) });
+    let reason: string;
+    try {
+      reason = err instanceof Error ? err.message : String(err);
+    } catch {
+      reason = 'unreadable thrown value';
+    }
+    logger.error('DB save image failed', { error: reason });
     throw new AppError(
       'The verification attestation could not be recorded. No document was accepted.',
       500,
diff --git a/Blockchain/Dev/services/kyc/src/__tests__/ks1868-kyc-save-image-attestation-unreadable-throw.test.ts b/Blockchain/Dev/services/kyc/src/__tests__/ks1868-kyc-save-image-attestation-unreadable-throw.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/kyc/src/__tests__/ks1868-kyc-save-image-attestation-unreadable-throw.test.ts
@@ -0,0 +1,215 @@
+import { describe, it, expect, vi, beforeAll, beforeEach, afterAll } from 'vitest';
+import http from 'http';
+import { randomUUID } from 'crypto';
+
+process.env.KYC_PROVIDER = 'mock';
+process.env.NODE_ENV = 'test';
+
+// KS-1868: `dbSaveImage` must still log its line and answer the authored attestation failure
+// (500 KYC_ATTESTATION_WRITE_FAILED) when the thrown value itself cannot be read (a revoked Proxy throws
+// on `instanceof`; an Error whose `message` getter throws, throws on `.message`). Harness: the KS-1845 one
+// (real app on a real listener, db and subject-DEK modules replaced, an in-memory verification table).
+// The db stand-in rejects with a plain function, not a vi.fn(): a spy inspects what it rejects with and could
+// itself fail on a revoked Proxy before the code under test saw it.
+const h = vi.hoisted(() => ({
+  toThrow: undefined as unknown,
+  failImages: false,
+  logged: [] as unknown[][],
+  table: new Map<string, Record<string, any>>(),
+  upserts: 0,
+  imageInserts: 0,
+}));
+
+const COLS = [
+  'id', 'user_id', 'requested_level', 'current_level', 'status', 'provider',
+  'provider_application_id', 'provider_check_id', 'documents', 'liveness_completed',
+  'liveness_score', 'checks', 'overall_score', 'risk_level', 'reviewed_by',
+  'review_notes', 'consent_given', 'consent_timestamp', 'data_retention_expiry',
+  'created_at', 'updated_at', 'completed_at', 'expires_at',
+];
+
+vi.mock('../db', () => ({
+  initDb: async () => undefined,
+  isDbAvailable: () => true,
+  query: async (sql: string, params: any[] = []) => {
+    const s = String(sql);
+    if (/INSERT\s+INTO\s+svc_kyc_images/i.test(s)) {
+      h.imageInserts += 1;
+      if (h.failImages) throw h.toThrow;
+      return { rows: [] };
+    }
+    if (/INSERT\s+INTO\s+svc_kyc_verifications/i.test(s)) {
+      const incoming: Record<string, any> = {};
+      COLS.forEach((c, i) => { incoming[c] = params[i]; });
+      h.upserts += 1;
+      h.table.set(incoming.id, incoming);
+      return { rows: [] };
+    }
+    if (/SELECT\s+\*\s+FROM\s+svc_kyc_verifications/i.test(s)) {
+      const found = h.table.get(params[0]);
+      return { rows: found ? [{ ...found }] : [] };
+    }
+    return { rows: [] };
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
+  const logger = {
+    info: () => undefined,
+    warn: () => undefined,
+    debug: () => undefined,
+    error: (...args: unknown[]) => {
+      h.logged.push(args);
+    },
+  };
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
+/** A real 1x1 PNG, because the image sniffing is not replaced. */
+const PNG_B64 =
+  'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg==';
+
+const TIMEOUT_MS = 2500;
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
+async function callRoute(path: string, body: unknown) {
+  const res = await fetch(origin + path, {
+    method: 'POST',
+    headers: { 'Content-Type': 'application/json' },
+    body: JSON.stringify(body),
+    signal: AbortSignal.timeout(TIMEOUT_MS),
+  }).catch(() => undefined);
+  if (!res) return undefined;
+  const parsed: any = await res.json().catch(() => undefined);
+  return { status: res.status, body: parsed };
+}
+
+async function seedVerification(): Promise<string> {
+  const init = await callRoute('/api/kyc/initiate', { userId: randomUUID(), requestedLevel: 'BASIC', consentGiven: true });
+  expect(init?.status).toBe(201);
+  return init?.body?.data?.verificationId as string;
+}
+
+const LINES = () => h.logged.filter((c) => String(c[0]).includes('DB save image failed'));
+const parseDocs = (raw: unknown): unknown[] => (typeof raw === 'string' ? JSON.parse(raw) : ((raw as unknown[]) ?? []));
+
+afterAll(async () => {
+  if (httpServer) {
+    (httpServer as http.Server & { closeAllConnections?: () => void }).closeAllConnections?.();
+    await new Promise<void>((resolve) => httpServer.close(() => resolve()));
+  }
+});
+
+describe('KS-1868 dbSaveImage reads the thrown value safely', () => {
+  beforeAll(async () => {
+    await startApp();
+  }, 120_000);
+
+  beforeEach(() => {
+    h.toThrow = undefined;
+    h.failImages = true;
+    h.logged.length = 0;
+    h.table.clear();
+    h.upserts = 0;
+    h.imageInserts = 0;
+  });
+
+  async function submitDocument() {
+    const id = await seedVerification();
+    const upsertsBefore = h.upserts;
+    const res = await callRoute('/api/kyc/' + id + '/document', {
+      verificationId: id,
+      documentType: 'passport',
+      country: 'GB',
+      frontImage: PNG_B64,
+    });
+    return { id, res, upsertsBefore };
+  }
+
+  function expectNothingRecorded(id: string, upsertsBefore: number) {
+    expect(h.imageInserts).toBe(1);
+    expect(h.upserts).toBe(upsertsBefore);
+    const stored = h.table.get(id);
+    expect(parseDocs(stored?.documents)).toHaveLength(0);
+    expect(stored?.status).toBe('pending');
+  }
+
+  it('control ks1868 C1 an ordinary Error still logs its message and the upload is refused with the attestation failure', async () => {
+    h.toThrow = new Error('db down');
+    const { id, res, upsertsBefore } = await submitDocument();
+    expect(res?.status).toBe(500);
+    expect(JSON.stringify(res?.body)).toContain('KYC_ATTESTATION_WRITE_FAILED');
+    expect(LINES()).toHaveLength(1);
+    expect(LINES()[0][1]).toEqual({ error: 'db down' });
+    expectNothingRecorded(id, upsertsBefore);
+  });
+
+  it('RED ks1868 R1 a revoked Proxy thrown value logs a constant reason and the upload is refused with the attestation failure', async () => {
+    const { proxy, revoke } = Proxy.revocable({}, {});
+    revoke();
+    h.toThrow = proxy;
+    const { id, res, upsertsBefore } = await submitDocument();
+    expect(res?.status).toBe(500);
+    expect(JSON.stringify(res?.body)).toContain('KYC_ATTESTATION_WRITE_FAILED');
+    expect(LINES()).toHaveLength(1);
+    expect(LINES()[0][1]).toEqual({ error: 'unreadable thrown value' });
+    expectNothingRecorded(id, upsertsBefore);
+  });
+
+  it('RED ks1868 R2 an Error whose message getter throws logs a constant reason and the upload is refused with the attestation failure', async () => {
+    h.toThrow = Object.create(Error.prototype, {
+      message: {
+        get() {
+          throw new Error('getter boom');
+        },
+      },
+    });
+    const { id, res, upsertsBefore } = await submitDocument();
+    expect(res?.status).toBe(500);
+    expect(JSON.stringify(res?.body)).toContain('KYC_ATTESTATION_WRITE_FAILED');
+    expect(LINES()).toHaveLength(1);
+    expect(LINES()[0][1]).toEqual({ error: 'unreadable thrown value' });
+    expectNothingRecorded(id, upsertsBefore);
+  });
+});
```
