# READY — KS-1970-KS-1970-O122-P1 (Spark (DeepSeek V4 Flash), briefed, code_patch2, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-10_ks_1970_o121_p1_auth_issuer_cert_sweep_three_fire_and_forget_catches_read_a_hostile_thrown_value/out.md.checker/patch.diff`** (from `ls` at 00:14 2026-11-10; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-10_ks_1970_o121_p1_auth_issuer_cert_sweep_three_fire_and_forget_catches_read_a_hostile_thrown_value/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-10_ks_1970_o121_p1_auth_issuer_cert_sweep_three_fire_and_forget_catches_read_a_hostile_thrown_value/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-10_ks_1970_o121_p1_auth_issuer_cert_sweep_three_fire_and_forget_catches_read_a_hostile_thrown_value/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-09_ks_1970_o121_p1_auth_issuer_cert_sweep_three_fire_and_forget_catches_read_a_hostile_thrown_value-control-r5/out.md.checker/patch.diff` rc 0, Wednesday).

**Held 00:14 2026-11-10 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-10_ks_1970_o121_p1_auth_issuer_cert_sweep_three_fire_and_forget_catches_read_a_hostile_thrown_value/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `d0b4825cc24493213f82b609670a4a0fa521a4b9`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/services/auth/src/services/issuerCertSweep.ts } + { Blockchain/Dev/services/auth/src/__tests__/ks1970-issuer-cert-sweep-fire-and-forget-catches-read-a-hostile-thrown-value.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/auth/src/services/issuerCertSweep.ts` (product) and `Blockchain/Dev/services/auth/src/__tests__/ks1970-issuer-cert-sweep-fire-and-forget-catches-read-a-hostile-thrown-value.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
31	13	Blockchain/Dev/services/auth/src/services/issuerCertSweep.ts
330	0	Blockchain/Dev/services/auth/src/__tests__/ks1970-issuer-cert-sweep-fire-and-forget-catches-read-a-hostile-thrown-value.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (31 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: issuerCertSweep.ts`
- CODE_PATCH2 (rung 3, 1 product files + 1 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/services/auth/src/services/issuerCertSweep.ts`; test(s): `Blockchain/Dev/services/auth/src/__tests__/ks1970-issuer-cert-sweep-fire-and-forget-catches-read-a-hostile-thrown-value.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/services/auth/src/services/issuerCertSweep.ts 31 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/auth/src/__tests__/ks1970-issuer-cert-sweep-fire-and-forget-catches-read-a-hostile-thrown-value.test.ts 330 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/auth/src/services/issuerCertSweep.ts` (hunks=2, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/auth/src/__tests__/ks1970-issuer-cert-sweep-fire-and-forget-catches-read-a-hostile-thrown-value.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (12 failed / 18 run; controls green; assertion reds)` [red_first.json: failed=12 of total=18; red cell(s): ['KS-1868 the issuer cert sweep fire-and-forget catches log text for a hostile thrown value RED ks1868 R1 ISSUER_CERT_EXPIRING_SOON publish: a rejection that is a revoked Proxy is logged as text and the sweep goes on as it does for an ordinary Error', 'KS-1868 the issuer cert sweep fire-and-forget catches log text for a hostile thrown value RED ks1868 R2 ISSUER_CERT_EXPIRING_SOON publish: a rejection that is an Error whose message getter throws is logged as text and the sweep goes on as it does for an ordinary Error', 'KS-1868 the issuer cert sweep fire-and-forget catches log text for a hostile thrown value RED ks1868 R3 ISSUER_CERT_EXPIRING_SOON publish: a rejection that is an Error whose message is a null-prototype object is logged as text and the sweep goes on as it does for an ordinary Error', 'KS-1868 the issuer cert sweep fire-and-forget catches log text for a hostile thrown value RED ks1868 R4 ISSUER_CERT_EXPIRING_SOON publish: a rejection that is an Error whose message is a Symbol is logged as text and the sweep goes on as it does for an ordinary Error', 'KS-1868 the issuer cert sweep fire-and-forget catches log text for a hostile thrown value RED ks1868 R5 startup sweep: a rejection that is a revoked Proxy is logged as text and the sweep goes on as it does for an ordinary Error', 'KS-1868 the issuer cert sweep fire-and-forget catches log text for a hostile thrown value RED ks1868 R6 startup sweep: a rejection that is an Error whose message getter throws is logged as text and the sweep goes on as it does for an ordinary Error', 'KS-1868 the issuer cert sweep fire-and-forget catches log text for a hostile thrown value RED ks1868 R7 startup sweep: a rejection that is an Error whose message is a null-prototype object is logged as text and the sweep goes on as it does for an ordinary Error', 'KS-1868 the issuer cert sweep fire-and-forget catches log text for a hostile thrown value RED ks1868 R8 startup sweep: a rejection that is an Error whose message is a Symbol is logged as text and the sweep goes on as it does for an ordinary Error', 'KS-1868 the issuer cert sweep fire-and-forget catches log text for a hostile thrown value RED ks1970 R9 scheduled sweep: a rejection that is a revoked Proxy is logged as text and nothing is unhandled', 'KS-1868 the issuer cert sweep fire-and-forget catches log text for a hostile thrown value RED ks1970 R10 scheduled sweep: a rejection that is an Error whose message getter throws is logged as text and nothing is unhandled', 'KS-1868 the issuer cert sweep fire-and-forget catches log text for a hostile thrown value RED ks1970 R11 scheduled sweep: a rejection that is an Error whose message is a null-prototype object is logged as text and nothing is unhandled', 'KS-1868 the issuer cert sweep fire-and-forget catches log text for a hostile thrown value RED ks1970 R12 scheduled sweep: a rejection that is an Error whose message is a Symbol is logged as text and nothing is unhandled']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 1 product section(s) (18 passed / 18 run)` [green_after.json: failed=0 of total=18, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=1837 failed=3 | after: total=1855 failed=3` · `NEW reds: []` [baseline_suite.json total=1837 failed=3; after_suite.json total=1855 failed=3]
- A6 [verbatim]: `PASS A6 whole services/auth suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/auth: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 products=1 tests=1 red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/auth/src/services/issuerCertSweep.ts` (+31/-13 per numstat.out) and the test file `Blockchain/Dev/services/auth/src/__tests__/ks1970-issuer-cert-sweep-fire-and-forget-catches-read-a-hostile-thrown-value.test.ts` (+330/-0); 2 files in all (code_patch2: products Blockchain/Dev/services/auth/src/services/issuerCertSweep.ts). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `d0b4825cc24493213f82b609670a4a0fa521a4b9` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-10_ks_1970_o121_p1_auth_issuer_cert_sweep_three_fire_and_forget_catches_read_a_hostile_thrown_value/input.json`. brief NOT LOCATED under night/briefs/ (no claim made). Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-10_ks_1970_o121_p1_auth_issuer_cert_sweep_three_fire_and_forget_catches_read_a_hostile_thrown_value/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/auth/src/services/issuerCertSweep.ts b/Blockchain/Dev/services/auth/src/services/issuerCertSweep.ts
--- a/Blockchain/Dev/services/auth/src/services/issuerCertSweep.ts
+++ b/Blockchain/Dev/services/auth/src/services/issuerCertSweep.ts
@@ -125,11 +125,17 @@
         validUntil: row.validUntil.toISOString(),
         daysRemaining: days,
-      }).catch((err) =>
+      }).catch((err) => {
+        let reason: string;
+        try {
+          reason = String(err instanceof Error ? err.message : err);
+        } catch {
+          reason = 'unreadable thrown value';
+        }
         logger.warn('publishEvent ISSUER_CERT_EXPIRING_SOON failed', {
           certId: row.id,
           daysRemaining: days,
-          error: err instanceof Error ? err.message : String(err),
-        }),
-      );
+          error: reason,
+        });
+      });
     }
   }
@@ -169,17 +175,29 @@
   // Run once at startup so any cert that expired while the service was
   // down gets caught immediately. Errors are logged inside runIssuerCertSweep.
-  runIssuerCertSweep().catch((err) =>
+  runIssuerCertSweep().catch((err) => {
+    let reason: string;
+    try {
+      reason = String(err instanceof Error ? err.message : err);
+    } catch {
+      reason = 'unreadable thrown value';
+    }
     logger.error('Initial issuer cert sweep failed', {
-      error: err instanceof Error ? err.message : String(err),
-    }),
-  );
-
+      error: reason,
+    });
+  });
+  // KS-1970: the scheduled tick below has its own .catch, guarded the same way.
   if (effectiveInterval > 0) {
     sweepTimer = setInterval(() => {
-      runIssuerCertSweep().catch((err) =>
+      runIssuerCertSweep().catch((err) => {
+        let reason: string;
+        try {
+          reason = String(err instanceof Error ? err.message : err);
+        } catch {
+          reason = 'unreadable thrown value';
+        }
         logger.error('Scheduled issuer cert sweep failed', {
-          error: err instanceof Error ? err.message : String(err),
-        }),
-      );
+          error: reason,
+        });
+      });
     }, effectiveInterval);
     logger.info('Issuer cert sweep scheduled', { intervalMs: effectiveInterval });
diff --git a/Blockchain/Dev/services/auth/src/__tests__/ks1970-issuer-cert-sweep-fire-and-forget-catches-read-a-hostile-thrown-value.test.ts b/Blockchain/Dev/services/auth/src/__tests__/ks1970-issuer-cert-sweep-fire-and-forget-catches-read-a-hostile-thrown-value.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/auth/src/__tests__/ks1970-issuer-cert-sweep-fire-and-forget-catches-read-a-hostile-thrown-value.test.ts
@@ -0,0 +1,330 @@
+import { describe, it, expect, beforeAll, afterAll, beforeEach, afterEach, vi } from 'vitest';
+
+// KS-1970 (re-spin of the held O89-P6, now also the scheduled sweep): the fire-and-forget catches in services/auth/src/services/issuerCertSweep.ts log
+// `{ error: err instanceof Error ? err.message : String(err) }` with the read INSIDE the logger call's arguments, unguarded.
+// A thrown value whose read throws (a revoked Proxy, an Error whose message getter throws) makes the catch itself throw; an Error
+// whose message is readable but not a string (a null-prototype object, a Symbol) is handed to the logger as is. The cells make the
+// repository, the event bus or the platform scope reject with such a value and assert the line is logged as text (the constant
+// when the value cannot be turned into text) and that the sweep goes on exactly as it does for an ordinary Error. Harness: the
+// real sweep module with the logger, event bus, repository and shared scope replaced by plain stand-ins (no database, no network).
+const h = vi.hoisted(() => ({
+  toThrow: undefined as unknown,
+  expiredFail: false,
+  soonFailDays: 0,
+  expiredRows: [] as unknown[],
+  soonRows: {} as Record<number, unknown[]>,
+  soonCalls: [] as number[],
+  published: [] as string[],
+  expiredPublishFails: false,
+  soonPublishFails: false,
+  scopeFails: false,
+  logged: [] as unknown[][],
+  unhandled: 0,
+}));
+
+const capture = vi.hoisted(() => ({
+  debug: () => undefined,
+  info: () => undefined,
+  warn: (...args: unknown[]) => {
+    h.logged.push(['warn', ...args]);
+  },
+  error: (...args: unknown[]) => {
+    h.logged.push(['error', ...args]);
+  },
+  log: () => undefined,
+}));
+vi.mock('../utils/logger', () => ({ logger: capture, createLogger: () => capture, validateEnv: () => undefined }));
+vi.mock('@secuura/shared', () => ({
+  runWithPlatformScope: (fn: () => Promise<unknown>) => (h.scopeFails ? Promise.reject(h.toThrow) : fn()),
+}));
+vi.mock('../events', () => ({
+  EventTypes: { ISSUER_CERT_EXPIRED: 'EXPIRED', ISSUER_CERT_EXPIRING_SOON: 'SOON' },
+  publishEvent: (type: string) => {
+    h.published.push(type);
+    if ((type === 'EXPIRED' && h.expiredPublishFails) || (type === 'SOON' && h.soonPublishFails)) {
+      return Promise.reject(h.toThrow);
+    }
+    return Promise.resolve(undefined);
+  },
+}));
+vi.mock('../repositories/issuerCertRepo', () => ({
+  markExpiredCerts: () => (h.expiredFail ? Promise.reject(h.toThrow) : Promise.resolve(h.expiredRows)),
+  findExpiringSoon: (days: number) => {
+    h.soonCalls.push(days);
+    if (h.soonFailDays === days) return Promise.reject(h.toThrow);
+    return Promise.resolve(h.soonRows[days] ?? []);
+  },
+}));
+
+const SAVED_LISTENERS = process.listeners('unhandledRejection');
+const onUnhandled = () => {
+  h.unhandled += 1;
+};
+const SAVED_INTERVAL_ENV = process.env.ISSUER_CERT_SWEEP_INTERVAL_MS;
+
+let mod: typeof import('../services/issuerCertSweep');
+beforeAll(async () => {
+  process.removeAllListeners('unhandledRejection');
+  process.on('unhandledRejection', onUnhandled);
+  mod = await import('../services/issuerCertSweep');
+});
+afterAll(() => {
+  process.removeListener('unhandledRejection', onUnhandled);
+  for (const l of SAVED_LISTENERS) process.on('unhandledRejection', l as (...a: any[]) => void);
+  if (SAVED_INTERVAL_ENV === undefined) delete process.env.ISSUER_CERT_SWEEP_INTERVAL_MS;
+  else process.env.ISSUER_CERT_SWEEP_INTERVAL_MS = SAVED_INTERVAL_ENV;
+});
+beforeEach(() => {
+  delete process.env.ISSUER_CERT_SWEEP_INTERVAL_MS;
+  h.toThrow = undefined;
+  h.expiredFail = false;
+  h.soonFailDays = 0;
+  h.expiredRows = [];
+  h.soonRows = {};
+  h.soonCalls.length = 0;
+  h.published.length = 0;
+  h.expiredPublishFails = false;
+  h.soonPublishFails = false;
+  h.scopeFails = false;
+  h.logged.length = 0;
+  h.unhandled = 0;
+});
+afterEach(() => {
+  mod.stopIssuerCertSweep();
+});
+
+const row = (id: string) => ({
+  id,
+  tenantId: 'ten-1868',
+  fingerprintSha256: 'fp-' + id,
+  name: 'name-' + id,
+  validUntil: new Date('2026-12-01T00:00:00.000Z'),
+});
+const flush = () => new Promise<void>((resolve) => setTimeout(resolve, 30));
+async function run(): Promise<{ ok: boolean; value: unknown }> {
+  try {
+    return { ok: true, value: await mod.runIssuerCertSweep() };
+  } catch {
+    return { ok: false, value: undefined };
+  }
+}
+const LINES = (level: string, msg: string) => h.logged.filter((c) => c[0] === level && c[1] === msg);
+/** The logged `error` field as a string; the type name when it is not one (a hostile value never reaches an assertion). */
+const reasonOf = (c: unknown[] | undefined): string => {
+  const v = (c?.[2] as { error?: unknown } | undefined)?.error;
+  return typeof v === 'string' ? v : '<' + typeof v + '>';
+};
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
+// KS-1970: the scheduled sweep's own .catch (the setInterval tick). The interval is long enough that the first tick lands once between two polls.
+async function startAndWaitForScheduled(): Promise<void> {
+  h.scopeFails = true;
+  mod.startIssuerCertSweep(100);
+  for (let i = 0; i < 40 && LINES('error', 'Scheduled issuer cert sweep failed').length < 1 && h.unhandled < 2; i++) await flush();
+  mod.stopIssuerCertSweep();
+  await flush();
+}
+
+describe('KS-1868 the issuer cert sweep fire-and-forget catches log text for a hostile thrown value', () => {
+  it('control ks1868 C1 the ISSUER_CERT_EXPIRING_SOON publish: an ordinary Error is logged as a warning with its message and nothing is unhandled', async () => {
+    h.soonRows = { 30: [row('c30')] };
+    h.soonPublishFails = true;
+    h.toThrow = new Error('bus down');
+    expect(await run()).toEqual({ ok: true, value: { expired: 0, expiringSoon: { 30: 1, 7: 0, 1: 0 } } });
+    await flush();
+    expect(h.unhandled).toBe(0);
+    expect(LINES('warn', 'publishEvent ISSUER_CERT_EXPIRING_SOON failed')).toHaveLength(1);
+    expect(reasonOf(LINES('warn', 'publishEvent ISSUER_CERT_EXPIRING_SOON failed')[0])).toBe('bus down');
+    expect((LINES('warn', 'publishEvent ISSUER_CERT_EXPIRING_SOON failed')[0]?.[2] as { daysRemaining?: number } | undefined)?.daysRemaining).toBe(30);
+  });
+  it('control ks1868 C2 the ISSUER_CERT_EXPIRING_SOON publish: a thrown plain string is logged as a warning with its own text', async () => {
+    h.soonRows = { 30: [row('c30')] };
+    h.soonPublishFails = true;
+    h.toThrow = 'plain boom';
+    expect(await run()).toEqual({ ok: true, value: { expired: 0, expiringSoon: { 30: 1, 7: 0, 1: 0 } } });
+    await flush();
+    expect(h.unhandled).toBe(0);
+    expect(LINES('warn', 'publishEvent ISSUER_CERT_EXPIRING_SOON failed')).toHaveLength(1);
+    expect(reasonOf(LINES('warn', 'publishEvent ISSUER_CERT_EXPIRING_SOON failed')[0])).toBe('plain boom');
+    expect((LINES('warn', 'publishEvent ISSUER_CERT_EXPIRING_SOON failed')[0]?.[2] as { daysRemaining?: number } | undefined)?.daysRemaining).toBe(30);
+  });
+  it('control ks1868 C3 the startup sweep: an ordinary Error is logged with its message ', async () => {
+    h.scopeFails = true;
+    h.toThrow = new Error('scope down');
+    mod.startIssuerCertSweep(0);
+    for (let i = 0; i < 40 && LINES('error', 'Initial issuer cert sweep failed').length < 1; i++) await flush();
+    mod.stopIssuerCertSweep();
+    await flush();
+    expect(h.unhandled).toBe(0);
+    expect(LINES('error', 'Initial issuer cert sweep failed')).toHaveLength(1);
+    expect(reasonOf(LINES('error', 'Initial issuer cert sweep failed')[0])).toBe('scope down');
+    expect(LINES('error', 'Scheduled issuer cert sweep failed')).toHaveLength(0);
+  });
+  it('control ks1868 C4 the startup sweep: a thrown plain string is logged as its own text ', async () => {
+    h.scopeFails = true;
+    h.toThrow = 'plain boom';
+    mod.startIssuerCertSweep(0);
+    for (let i = 0; i < 40 && LINES('error', 'Initial issuer cert sweep failed').length < 1; i++) await flush();
+    mod.stopIssuerCertSweep();
+    await flush();
+    expect(h.unhandled).toBe(0);
+    expect(LINES('error', 'Initial issuer cert sweep failed')).toHaveLength(1);
+    expect(reasonOf(LINES('error', 'Initial issuer cert sweep failed')[0])).toBe('plain boom');
+    expect(LINES('error', 'Scheduled issuer cert sweep failed')).toHaveLength(0);
+  });
+  it('RED ks1868 R1 ISSUER_CERT_EXPIRING_SOON publish: a rejection that is a revoked Proxy is logged as text and the sweep goes on as it does for an ordinary Error', async () => {
+    h.soonRows = { 30: [row('c30')] };
+    h.soonPublishFails = true;
+    h.toThrow = SHAPES[0][1]();
+    expect(await run()).toEqual({ ok: true, value: { expired: 0, expiringSoon: { 30: 1, 7: 0, 1: 0 } } });
+    await flush();
+    expect(h.unhandled).toBe(0);
+    expect(LINES('warn', 'publishEvent ISSUER_CERT_EXPIRING_SOON failed')).toHaveLength(1);
+    expect(reasonOf(LINES('warn', 'publishEvent ISSUER_CERT_EXPIRING_SOON failed')[0])).toBe(SHAPES[0][2]);
+    expect((LINES('warn', 'publishEvent ISSUER_CERT_EXPIRING_SOON failed')[0]?.[2] as { daysRemaining?: number } | undefined)?.daysRemaining).toBe(30);
+  });
+  it('RED ks1868 R2 ISSUER_CERT_EXPIRING_SOON publish: a rejection that is an Error whose message getter throws is logged as text and the sweep goes on as it does for an ordinary Error', async () => {
+    h.soonRows = { 30: [row('c30')] };
+    h.soonPublishFails = true;
+    h.toThrow = SHAPES[1][1]();
+    expect(await run()).toEqual({ ok: true, value: { expired: 0, expiringSoon: { 30: 1, 7: 0, 1: 0 } } });
+    await flush();
+    expect(h.unhandled).toBe(0);
+    expect(LINES('warn', 'publishEvent ISSUER_CERT_EXPIRING_SOON failed')).toHaveLength(1);
+    expect(reasonOf(LINES('warn', 'publishEvent ISSUER_CERT_EXPIRING_SOON failed')[0])).toBe(SHAPES[1][2]);
+    expect((LINES('warn', 'publishEvent ISSUER_CERT_EXPIRING_SOON failed')[0]?.[2] as { daysRemaining?: number } | undefined)?.daysRemaining).toBe(30);
+  });
+  it('RED ks1868 R3 ISSUER_CERT_EXPIRING_SOON publish: a rejection that is an Error whose message is a null-prototype object is logged as text and the sweep goes on as it does for an ordinary Error', async () => {
+    h.soonRows = { 30: [row('c30')] };
+    h.soonPublishFails = true;
+    h.toThrow = SHAPES[2][1]();
+    expect(await run()).toEqual({ ok: true, value: { expired: 0, expiringSoon: { 30: 1, 7: 0, 1: 0 } } });
+    await flush();
+    expect(h.unhandled).toBe(0);
+    expect(LINES('warn', 'publishEvent ISSUER_CERT_EXPIRING_SOON failed')).toHaveLength(1);
+    expect(reasonOf(LINES('warn', 'publishEvent ISSUER_CERT_EXPIRING_SOON failed')[0])).toBe(SHAPES[2][2]);
+    expect((LINES('warn', 'publishEvent ISSUER_CERT_EXPIRING_SOON failed')[0]?.[2] as { daysRemaining?: number } | undefined)?.daysRemaining).toBe(30);
+  });
+  it('RED ks1868 R4 ISSUER_CERT_EXPIRING_SOON publish: a rejection that is an Error whose message is a Symbol is logged as text and the sweep goes on as it does for an ordinary Error', async () => {
+    h.soonRows = { 30: [row('c30')] };
+    h.soonPublishFails = true;
+    h.toThrow = SHAPES[3][1]();
+    expect(await run()).toEqual({ ok: true, value: { expired: 0, expiringSoon: { 30: 1, 7: 0, 1: 0 } } });
+    await flush();
+    expect(h.unhandled).toBe(0);
+    expect(LINES('warn', 'publishEvent ISSUER_CERT_EXPIRING_SOON failed')).toHaveLength(1);
+    expect(reasonOf(LINES('warn', 'publishEvent ISSUER_CERT_EXPIRING_SOON failed')[0])).toBe(SHAPES[3][2]);
+    expect((LINES('warn', 'publishEvent ISSUER_CERT_EXPIRING_SOON failed')[0]?.[2] as { daysRemaining?: number } | undefined)?.daysRemaining).toBe(30);
+  });
+  it('RED ks1868 R5 startup sweep: a rejection that is a revoked Proxy is logged as text and the sweep goes on as it does for an ordinary Error', async () => {
+    h.scopeFails = true;
+    h.toThrow = SHAPES[0][1]();
+    mod.startIssuerCertSweep(0);
+    for (let i = 0; i < 40 && LINES('error', 'Initial issuer cert sweep failed').length < 1; i++) await flush();
+    mod.stopIssuerCertSweep();
+    await flush();
+    expect(h.unhandled).toBe(0);
+    expect(LINES('error', 'Initial issuer cert sweep failed')).toHaveLength(1);
+    expect(reasonOf(LINES('error', 'Initial issuer cert sweep failed')[0])).toBe(SHAPES[0][2]);
+    expect(LINES('error', 'Scheduled issuer cert sweep failed')).toHaveLength(0);
+  });
+  it('RED ks1868 R6 startup sweep: a rejection that is an Error whose message getter throws is logged as text and the sweep goes on as it does for an ordinary Error', async () => {
+    h.scopeFails = true;
+    h.toThrow = SHAPES[1][1]();
+    mod.startIssuerCertSweep(0);
+    for (let i = 0; i < 40 && LINES('error', 'Initial issuer cert sweep failed').length < 1; i++) await flush();
+    mod.stopIssuerCertSweep();
+    await flush();
+    expect(h.unhandled).toBe(0);
+    expect(LINES('error', 'Initial issuer cert sweep failed')).toHaveLength(1);
+    expect(reasonOf(LINES('error', 'Initial issuer cert sweep failed')[0])).toBe(SHAPES[1][2]);
+    expect(LINES('error', 'Scheduled issuer cert sweep failed')).toHaveLength(0);
+  });
+  it('RED ks1868 R7 startup sweep: a rejection that is an Error whose message is a null-prototype object is logged as text and the sweep goes on as it does for an ordinary Error', async () => {
+    h.scopeFails = true;
+    h.toThrow = SHAPES[2][1]();
+    mod.startIssuerCertSweep(0);
+    for (let i = 0; i < 40 && LINES('error', 'Initial issuer cert sweep failed').length < 1; i++) await flush();
+    mod.stopIssuerCertSweep();
+    await flush();
+    expect(h.unhandled).toBe(0);
+    expect(LINES('error', 'Initial issuer cert sweep failed')).toHaveLength(1);
+    expect(reasonOf(LINES('error', 'Initial issuer cert sweep failed')[0])).toBe(SHAPES[2][2]);
+    expect(LINES('error', 'Scheduled issuer cert sweep failed')).toHaveLength(0);
+  });
+  it('RED ks1868 R8 startup sweep: a rejection that is an Error whose message is a Symbol is logged as text and the sweep goes on as it does for an ordinary Error', async () => {
+    h.scopeFails = true;
+    h.toThrow = SHAPES[3][1]();
+    mod.startIssuerCertSweep(0);
+    for (let i = 0; i < 40 && LINES('error', 'Initial issuer cert sweep failed').length < 1; i++) await flush();
+    mod.stopIssuerCertSweep();
+    await flush();
+    expect(h.unhandled).toBe(0);
+    expect(LINES('error', 'Initial issuer cert sweep failed')).toHaveLength(1);
+    expect(reasonOf(LINES('error', 'Initial issuer cert sweep failed')[0])).toBe(SHAPES[3][2]);
+    expect(LINES('error', 'Scheduled issuer cert sweep failed')).toHaveLength(0);
+  });
+  it('control ks1970 C5 the scheduled sweep: an ordinary Error is logged with its message', async () => {
+    h.toThrow = new Error('scope down');
+    await startAndWaitForScheduled();
+    expect(h.unhandled).toBe(0);
+    expect(LINES('error', 'Scheduled issuer cert sweep failed')).toHaveLength(1);
+    expect(reasonOf(LINES('error', 'Scheduled issuer cert sweep failed')[0])).toBe('scope down');
+  });
+  it('control ks1970 C6 the scheduled sweep: a thrown plain string is logged as its own text', async () => {
+    h.toThrow = 'plain boom';
+    await startAndWaitForScheduled();
+    expect(h.unhandled).toBe(0);
+    expect(LINES('error', 'Scheduled issuer cert sweep failed')).toHaveLength(1);
+    expect(reasonOf(LINES('error', 'Scheduled issuer cert sweep failed')[0])).toBe('plain boom');
+  });
+  it('RED ks1970 R9 scheduled sweep: a rejection that is a revoked Proxy is logged as text and nothing is unhandled', async () => {
+    h.toThrow = SHAPES[0][1]();
+    await startAndWaitForScheduled();
+    expect(h.unhandled).toBe(0);
+    expect(LINES('error', 'Scheduled issuer cert sweep failed')).toHaveLength(1);
+    expect(reasonOf(LINES('error', 'Scheduled issuer cert sweep failed')[0])).toBe(SHAPES[0][2]);
+  });
+  it('RED ks1970 R10 scheduled sweep: a rejection that is an Error whose message getter throws is logged as text and nothing is unhandled', async () => {
+    h.toThrow = SHAPES[1][1]();
+    await startAndWaitForScheduled();
+    expect(h.unhandled).toBe(0);
+    expect(LINES('error', 'Scheduled issuer cert sweep failed')).toHaveLength(1);
+    expect(reasonOf(LINES('error', 'Scheduled issuer cert sweep failed')[0])).toBe(SHAPES[1][2]);
+  });
+  it('RED ks1970 R11 scheduled sweep: a rejection that is an Error whose message is a null-prototype object is logged as text and nothing is unhandled', async () => {
+    h.toThrow = SHAPES[2][1]();
+    await startAndWaitForScheduled();
+    expect(h.unhandled).toBe(0);
+    expect(LINES('error', 'Scheduled issuer cert sweep failed')).toHaveLength(1);
+    expect(reasonOf(LINES('error', 'Scheduled issuer cert sweep failed')[0])).toBe(SHAPES[2][2]);
+  });
+  it('RED ks1970 R12 scheduled sweep: a rejection that is an Error whose message is a Symbol is logged as text and nothing is unhandled', async () => {
+    h.toThrow = SHAPES[3][1]();
+    await startAndWaitForScheduled();
+    expect(h.unhandled).toBe(0);
+    expect(LINES('error', 'Scheduled issuer cert sweep failed')).toHaveLength(1);
+    expect(reasonOf(LINES('error', 'Scheduled issuer cert sweep failed')[0])).toBe(SHAPES[3][2]);
+  });
+});
```
