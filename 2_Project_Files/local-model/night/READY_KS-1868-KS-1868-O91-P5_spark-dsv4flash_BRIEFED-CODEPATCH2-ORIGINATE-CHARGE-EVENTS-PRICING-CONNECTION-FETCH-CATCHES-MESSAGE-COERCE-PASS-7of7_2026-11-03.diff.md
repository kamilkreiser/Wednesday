# READY — KS-1868-KS-1868-O91-P5 (spark-dsv4flash, briefed, code_patch2, jest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o91_p5_originate_charge_events_pricing_connection_and_fetch_catches_guard_message/out.md.checker/patch.diff`** (from `ls` at 07:26 2026-11-03; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o91_p5_originate_charge_events_pricing_connection_and_fetch_catches_guard_message/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o91_p5_originate_charge_events_pricing_connection_and_fetch_catches_guard_message/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o91_p5_originate_charge_events_pricing_connection_and_fetch_catches_guard_message/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o91_p5_originate_charge_events_pricing_connection_and_fetch_catches_guard_message-control/out.md.checker/patch.diff` rc 0, Wednesday).

**Held 07:26 2026-11-03 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o91_p5_originate_charge_events_pricing_connection_and_fetch_catches_guard_message/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `7ad0dcc14e5c565be7d7dbd0d24a357f3c3b06b6`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/services/originate/src/services/chargeEvents.ts } + { Blockchain/Dev/services/originate/src/__tests__/ks1868-originate-charge-events-pricing-connection-fetch-catches-unreadable-throw.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/originate/src/services/chargeEvents.ts` (product) and `Blockchain/Dev/services/originate/src/__tests__/ks1868-originate-charge-events-pricing-connection-fetch-catches-unreadable-throw.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
23	3	Blockchain/Dev/services/originate/src/services/chargeEvents.ts
146	0	Blockchain/Dev/services/originate/src/__tests__/ks1868-originate-charge-events-pricing-connection-fetch-catches-unreadable-throw.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (23 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: chargeEvents.ts`
- CODE_PATCH2 (rung 3, 1 product files + 1 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/services/originate/src/services/chargeEvents.ts`; test(s): `Blockchain/Dev/services/originate/src/__tests__/ks1868-originate-charge-events-pricing-connection-fetch-catches-unreadable-throw.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/services/originate/src/services/chargeEvents.ts 23 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/originate/src/__tests__/ks1868-originate-charge-events-pricing-connection-fetch-catches-unreadable-throw.test.ts 146 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/originate/src/services/chargeEvents.ts` (hunks=3, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/originate/src/__tests__/ks1868-originate-charge-events-pricing-connection-fetch-catches-unreadable-throw.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (6 failed / 9 run; controls green; assertion reds)` [red_first.json: failed=6 of total=9; red cell(s): ['KS-1868 the charge-event pricing, connection and fetch catches log text for a hostile thrown value RED ks1868 R1: a pricing failure that is a revoked Proxy is logged as text and loadPricing resolves, as for an ordinary Error', 'KS-1868 the charge-event pricing, connection and fetch catches log text for a hostile thrown value RED ks1868 R2: a pricing failure that is an Error whose message is a Symbol is logged as text and loadPricing resolves, as for an ordinary Error', 'KS-1868 the charge-event pricing, connection and fetch catches log text for a hostile thrown value RED ks1868 R3: a connection-check failure that is a revoked Proxy is logged as text and verifyDbReady rejects with the documented error, as for an ordinary Error', 'KS-1868 the charge-event pricing, connection and fetch catches log text for a hostile thrown value RED ks1868 R4: a connection-check failure that is an Error whose message getter throws is logged as text and verifyDbReady rejects with the documented error, as for an ordinary Error', 'KS-1868 the charge-event pricing, connection and fetch catches log text for a hostile thrown value RED ks1868 R5: a fetch failure that is a revoked Proxy is logged as text and rethrown as is, as for an ordinary Error', 'KS-1868 the charge-event pricing, connection and fetch catches log text for a hostile thrown value RED ks1868 R6: a fetch failure that is an Error whose message is a Symbol is logged as text and rethrown as is, as for an ordinary Error']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 1 product section(s) (9 passed / 9 run)` [green_after.json: failed=0 of total=9, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=2349 failed=11 | after: total=2358 failed=11` · `NEW reds: []` [baseline_suite.json total=2349 failed=11; after_suite.json total=2358 failed=11]
- A6 [verbatim]: `PASS A6 whole services/originate suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/originate: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 products=1 tests=1 red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/originate/src/services/chargeEvents.ts` (+23/-3 per numstat.out) and the test file `Blockchain/Dev/services/originate/src/__tests__/ks1868-originate-charge-events-pricing-connection-fetch-catches-unreadable-throw.test.ts` (+146/-0); 2 files in all (code_patch2: products Blockchain/Dev/services/originate/src/services/chargeEvents.ts). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `7ad0dcc14e5c565be7d7dbd0d24a357f3c3b06b6` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o91_p5_originate_charge_events_pricing_connection_and_fetch_catches_guard_message/input.json`. Brief (given by --brief; its `# ` heading names KS-1868): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1868_o91_p5_originate_charge_events_pricing_connection_and_fetch_catches_guard_message/KS-1868.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o91_p5_originate_charge_events_pricing_connection_and_fetch_catches_guard_message/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/originate/src/services/chargeEvents.ts b/Blockchain/Dev/services/originate/src/services/chargeEvents.ts
--- a/Blockchain/Dev/services/originate/src/services/chargeEvents.ts
+++ b/Blockchain/Dev/services/originate/src/services/chargeEvents.ts
@@ -79,6 +79,13 @@
       logger.info('Pricing loaded from database', { eventTypes: rows.length });
     }
   } catch (err: any) {
-    logger.warn('Failed to load pricing from DB, using defaults', { error: err?.message });
+    let reason: string | null | undefined;
+    try {
+      const m = err?.message;
+      reason = m === undefined || m === null ? m : String(m);
+    } catch {
+      reason = 'unreadable thrown value';
+    }
+    logger.warn('Failed to load pricing from DB, using defaults', { error: reason });
   }
 }
@@ -122,8 +129,14 @@
     await prisma.$queryRaw`SELECT 1`;
     logger.info('chargeEvents: database connection verified');
   } catch (err: any) {
+    let reason: string;
+    try {
+      reason = err instanceof Error ? err.message : String(err);
+    } catch {
+      reason = 'unreadable thrown value';
+    }
     logger.error('chargeEvents: database connection FAILED — charge events will not be available', {
-      error: err instanceof Error ? err.message : String(err),
+      error: reason,
     });
     throw new Error('Database is required for charge event operations');
   }
@@ -221,7 +234,14 @@
       createdAt: r.created_at?.toISOString?.() || r.created_at,
     }));
   } catch (err: any) {
-    logger.warn('Failed to fetch charge events from DB', { error: err?.message });
+    let reason: string | null | undefined;
+    try {
+      const m = err?.message;
+      reason = m === undefined || m === null ? m : String(m);
+    } catch {
+      reason = 'unreadable thrown value';
+    }
+    logger.warn('Failed to fetch charge events from DB', { error: reason });
     throw err;
   }
 }
diff --git a/Blockchain/Dev/services/originate/src/__tests__/ks1868-originate-charge-events-pricing-connection-fetch-catches-unreadable-throw.test.ts b/Blockchain/Dev/services/originate/src/__tests__/ks1868-originate-charge-events-pricing-connection-fetch-catches-unreadable-throw.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/originate/src/__tests__/ks1868-originate-charge-events-pricing-connection-fetch-catches-unreadable-throw.test.ts
@@ -0,0 +1,146 @@
+// KS-1868 (operator 91 screen, originate charge events): the pricing-load catch of loadPricing (line 82), the connection-check catch
+// of verifyDbReady (line 126) and the fetch catch of getChargeEventsByCertification (line 224) of
+// services/originate/src/services/chargeEvents.ts read the thrown value inside the logger call's arguments, unguarded
+// (`err?.message`, `err instanceof Error ? err.message : String(err)`). A thrown value whose read throws (a revoked Proxy, an Error
+// whose message getter throws) makes the catch itself throw: loadPricing REJECTS instead of keeping the default prices,
+// verifyDbReady rejects with the TypeError the read threw instead of its documented 'Database is required for charge event
+// operations' error, and getChargeEventsByCertification rejects with that TypeError instead of rethrowing the original value; an
+// Error whose message is readable but not a string (a Symbol) is handed to the logger uncoerced. The cells make the Prisma stand-in
+// reject with such a value and assert the ordinary outcome (resolve; the documented error; the original value) and a logged
+// line that carries text (the constant when the value cannot be turned into text). Harness: the real module with the Prisma
+// client of ../db replaced by a plain stand-in whose tagged-template query rejects with the value, and the logger by a plain
+// recording object (no database).
+const mockH: {
+  failure: { value: unknown } | undefined;
+  logs: { level: string; message: string; meta: Record<string, unknown> | undefined }[];
+} = { failure: undefined, logs: [] };
+
+jest.mock('../db', () => ({
+  prisma: {
+    $queryRaw: () => (mockH.failure ? Promise.reject(mockH.failure.value) : Promise.resolve([])),
+    $executeRaw: () => Promise.resolve(0),
+  },
+}));
+jest.mock('../utils/logger', () => {
+  const rec = (level: string) => (message: string, meta?: Record<string, unknown>) => {
+    mockH.logs.push({ level, message, meta });
+  };
+  return { logger: { debug: rec('debug'), info: rec('info'), warn: rec('warn'), error: rec('error') } };
+});
+
+type Ce = typeof import('../services/chargeEvents');
+const PRICING = 'Failed to load pricing from DB, using defaults';
+const CONN = 'chargeEvents: database connection FAILED — charge events will not be available';
+const FETCH = 'Failed to fetch charge events from DB';
+const DOCUMENTED = 'Database is required for charge event operations';
+
+beforeEach(() => {
+  mockH.failure = undefined;
+  mockH.logs.length = 0;
+});
+
+function freshCe(): Ce {
+  jest.resetModules();
+  // eslint-disable-next-line @typescript-eslint/no-require-imports
+  return require('../services/chargeEvents') as Ce;
+}
+async function pricing(value: unknown): Promise<{ ok: boolean }> {
+  mockH.failure = { value };
+  const ce = freshCe();
+  try {
+    await ce.loadPricing();
+    return { ok: true };
+  } catch {
+    return { ok: false };
+  }
+}
+async function conn(value: unknown): Promise<{ rejected: boolean; message: string }> {
+  mockH.failure = { value };
+  const ce = freshCe();
+  try {
+    await ce.verifyDbReady();
+    return { rejected: false, message: '' };
+  } catch (e) {
+    return { rejected: true, message: e instanceof Error ? e.message : '<not an Error>' };
+  }
+}
+async function fetchEvents(value: unknown): Promise<{ rejected: boolean; same: boolean }> {
+  mockH.failure = { value };
+  const ce = freshCe();
+  try {
+    await ce.getChargeEventsByCertification('cert_1', 'a0000000-0000-4000-8000-000000000001');
+    return { rejected: false, same: false };
+  } catch (e) {
+    return { rejected: true, same: Object.is(e, value) };
+  }
+}
+const LINES = (message: string) => mockH.logs.filter((l) => l.message === message);
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
+
+describe('KS-1868 the charge-event pricing, connection and fetch catches log text for a hostile thrown value', () => {
+  it('control ks1868 C1: an ordinary Error from the pricing query is logged with its message and loadPricing resolves', async () => {
+    expect(await pricing(new Error('pricing failed'))).toEqual({ ok: true });
+    expect(LINES(PRICING)).toHaveLength(1);
+    expect(reasonOf(LINES(PRICING)[0])).toBe('pricing failed');
+  });
+  it('control ks1868 C2: an ordinary Error from the connection check is logged with its message and verifyDbReady rejects with the documented error', async () => {
+    expect(await conn(new Error('conn failed'))).toEqual({ rejected: true, message: DOCUMENTED });
+    expect(LINES(CONN)).toHaveLength(1);
+    expect(reasonOf(LINES(CONN)[0])).toBe('conn failed');
+  });
+  it('control ks1868 C3: an ordinary Error from the fetch is logged with its message and rethrown as is', async () => {
+    expect(await fetchEvents(new Error('fetch failed'))).toEqual({ rejected: true, same: true });
+    expect(LINES(FETCH)).toHaveLength(1);
+    expect(reasonOf(LINES(FETCH)[0])).toBe('fetch failed');
+  });
+  it('RED ks1868 R1: a pricing failure that is a revoked Proxy is logged as text and loadPricing resolves, as for an ordinary Error', async () => {
+    expect(await pricing(revokedProxy())).toEqual({ ok: true });
+    expect(LINES(PRICING)).toHaveLength(1);
+    expect(reasonOf(LINES(PRICING)[0])).toBe('unreadable thrown value');
+  });
+  it('RED ks1868 R2: a pricing failure that is an Error whose message is a Symbol is logged as text and loadPricing resolves, as for an ordinary Error', async () => {
+    expect(await pricing(withMessage(Symbol('ks1868')))).toEqual({ ok: true });
+    expect(LINES(PRICING)).toHaveLength(1);
+    expect(reasonOf(LINES(PRICING)[0])).toBe('Symbol(ks1868)');
+  });
+  it('RED ks1868 R3: a connection-check failure that is a revoked Proxy is logged as text and verifyDbReady rejects with the documented error, as for an ordinary Error', async () => {
+    expect(await conn(revokedProxy())).toEqual({ rejected: true, message: DOCUMENTED });
+    expect(LINES(CONN)).toHaveLength(1);
+    expect(reasonOf(LINES(CONN)[0])).toBe('unreadable thrown value');
+  });
+  it('RED ks1868 R4: a connection-check failure that is an Error whose message getter throws is logged as text and verifyDbReady rejects with the documented error, as for an ordinary Error', async () => {
+    expect(await conn(getterThrows())).toEqual({ rejected: true, message: DOCUMENTED });
+    expect(LINES(CONN)).toHaveLength(1);
+    expect(reasonOf(LINES(CONN)[0])).toBe('unreadable thrown value');
+  });
+  it('RED ks1868 R5: a fetch failure that is a revoked Proxy is logged as text and rethrown as is, as for an ordinary Error', async () => {
+    expect(await fetchEvents(revokedProxy())).toEqual({ rejected: true, same: true });
+    expect(LINES(FETCH)).toHaveLength(1);
+    expect(reasonOf(LINES(FETCH)[0])).toBe('unreadable thrown value');
+  });
+  it('RED ks1868 R6: a fetch failure that is an Error whose message is a Symbol is logged as text and rethrown as is, as for an ordinary Error', async () => {
+    expect(await fetchEvents(withMessage(Symbol('ks1868')))).toEqual({ rejected: true, same: true });
+    expect(LINES(FETCH)).toHaveLength(1);
+    expect(reasonOf(LINES(FETCH)[0])).toBe('Symbol(ks1868)');
+  });
+});
```
