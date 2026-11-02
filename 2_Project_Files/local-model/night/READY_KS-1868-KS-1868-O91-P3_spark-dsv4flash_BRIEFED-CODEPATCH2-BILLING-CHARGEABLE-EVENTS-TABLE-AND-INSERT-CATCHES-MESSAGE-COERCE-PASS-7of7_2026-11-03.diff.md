# READY — KS-1868-KS-1868-O91-P3 (spark-dsv4flash, briefed, code_patch2, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o91_p3_billing_chargeable_events_table_and_insert_catches_guard_message/out.md.checker/patch.diff`** (from `ls` at 07:15 2026-11-03; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o91_p3_billing_chargeable_events_table_and_insert_catches_guard_message/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o91_p3_billing_chargeable_events_table_and_insert_catches_guard_message/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o91_p3_billing_chargeable_events_table_and_insert_catches_guard_message/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o91_p3_billing_chargeable_events_table_and_insert_catches_guard_message-control/out.md.checker/patch.diff` rc 0, Wednesday).

**Held 07:15 2026-11-03 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o91_p3_billing_chargeable_events_table_and_insert_catches_guard_message/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `26955bf1b828113fcfe29b6bd6e371dbe28b5360`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/services/billing/src/chargeable-events.ts } + { Blockchain/Dev/services/billing/src/__tests__/ks1868-billing-chargeable-events-catches-unreadable-throw.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/billing/src/chargeable-events.ts` (product) and `Blockchain/Dev/services/billing/src/__tests__/ks1868-billing-chargeable-events-catches-unreadable-throw.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
24	3	Blockchain/Dev/services/billing/src/chargeable-events.ts
150	0	Blockchain/Dev/services/billing/src/__tests__/ks1868-billing-chargeable-events-catches-unreadable-throw.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (24 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: chargeable-events.ts`
- CODE_PATCH2 (rung 3, 1 product files + 1 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/services/billing/src/chargeable-events.ts`; test(s): `Blockchain/Dev/services/billing/src/__tests__/ks1868-billing-chargeable-events-catches-unreadable-throw.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/services/billing/src/chargeable-events.ts 24 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/billing/src/__tests__/ks1868-billing-chargeable-events-catches-unreadable-throw.test.ts 150 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/billing/src/chargeable-events.ts` (hunks=3, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/billing/src/__tests__/ks1868-billing-chargeable-events-catches-unreadable-throw.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (6 failed / 9 run; controls green; assertion reds)` [red_first.json: failed=6 of total=9; red cell(s): ['KS-1868 the charge-event table and insert catches log text for a hostile thrown value RED ks1868 R1: a table bootstrap failure that is a revoked Proxy is logged as text and the INSERT still runs, as for an ordinary Error', 'KS-1868 the charge-event table and insert catches log text for a hostile thrown value RED ks1868 R2: a table bootstrap failure that is an Error whose message is a Symbol is logged as text and the INSERT still runs, as for an ordinary Error', 'KS-1868 the charge-event table and insert catches log text for a hostile thrown value RED ks1868 R3: a table verify failure that is an Error whose message getter throws resolves and is logged as text, as for an ordinary Error', 'KS-1868 the charge-event table and insert catches log text for a hostile thrown value RED ks1868 R4: a table verify failure that is a revoked Proxy resolves and is logged as text, as for an ordinary Error', 'KS-1868 the charge-event table and insert catches log text for a hostile thrown value RED ks1868 R5: an INSERT failure that is a revoked Proxy is logged as text and the event is still returned, as for an ordinary Error', 'KS-1868 the charge-event table and insert catches log text for a hostile thrown value RED ks1868 R6: an INSERT failure that is an Error whose message is a Symbol is logged as text and the event is still returned, as for an ordinary Error']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 1 product section(s) (9 passed / 9 run)` [green_after.json: failed=0 of total=9, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=368 failed=0 | after: total=377 failed=0` · `NEW reds: []` [baseline_suite.json total=368 failed=0; after_suite.json total=377 failed=0]
- A6 [verbatim]: `PASS A6 whole services/billing suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/billing: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 products=1 tests=1 red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/billing/src/chargeable-events.ts` (+24/-3 per numstat.out) and the test file `Blockchain/Dev/services/billing/src/__tests__/ks1868-billing-chargeable-events-catches-unreadable-throw.test.ts` (+150/-0); 2 files in all (code_patch2: products Blockchain/Dev/services/billing/src/chargeable-events.ts). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `26955bf1b828113fcfe29b6bd6e371dbe28b5360` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o91_p3_billing_chargeable_events_table_and_insert_catches_guard_message/input.json`. Brief (given by --brief; its `# ` heading names KS-1868): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1868_o91_p3_billing_chargeable_events_table_and_insert_catches_guard_message/KS-1868.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o91_p3_billing_chargeable_events_table_and_insert_catches_guard_message/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/billing/src/chargeable-events.ts b/Blockchain/Dev/services/billing/src/chargeable-events.ts
--- a/Blockchain/Dev/services/billing/src/chargeable-events.ts
+++ b/Blockchain/Dev/services/billing/src/chargeable-events.ts
@@ -59,6 +59,13 @@
     tableEnsured = true;
     logger.info('billing_charge_events table ensured');
   } catch (err: any) {
-    logger.warn('Failed to ensure billing_charge_events table', { error: err?.message });
+    let reason: string | null | undefined;
+    try {
+      const m = err?.message;
+      reason = m === undefined || m === null ? m : String(m);
+    } catch {
+      reason = 'unreadable thrown value';
+    }
+    logger.warn('Failed to ensure billing_charge_events table', { error: reason });
   }
 }
@@ -121,6 +128,13 @@
     ));
     logger.info('billing_charge_events table ready', { rowCount: result.rows[0]?.cnt ?? '0' });
   } catch (err: any) {
-    logger.warn('Failed to verify billing_charge_events table', { error: err?.message });
+    let reason: string | null | undefined;
+    try {
+      const m = err?.message;
+      reason = m === undefined || m === null ? m : String(m);
+    } catch {
+      reason = 'unreadable thrown value';
+    }
+    logger.warn('Failed to verify billing_charge_events table', { error: reason });
   }
 }
@@ -175,5 +189,12 @@
       logger.warn('DB not available — charge event not persisted', { eventId: id });
     }
   } catch (err: any) {
-    logger.warn('DB insert failed for charge event', { error: err?.message, eventId: id });
+    let reason: string | null | undefined;
+    try {
+      const m = err?.message;
+      reason = m === undefined || m === null ? m : String(m);
+    } catch {
+      reason = 'unreadable thrown value';
+    }
+    logger.warn('DB insert failed for charge event', { error: reason, eventId: id });
   }
diff --git a/Blockchain/Dev/services/billing/src/__tests__/ks1868-billing-chargeable-events-catches-unreadable-throw.test.ts b/Blockchain/Dev/services/billing/src/__tests__/ks1868-billing-chargeable-events-catches-unreadable-throw.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/billing/src/__tests__/ks1868-billing-chargeable-events-catches-unreadable-throw.test.ts
@@ -0,0 +1,150 @@
+import { describe, it, expect, beforeEach, vi } from 'vitest';
+
+// KS-1868 (operator 91 screen, billing chargeable events): the table-bootstrap catch of ensureTable (line 62), the table-verify
+// catch of loadChargeEventsFromDb (line 124) and the insert catch of createChargeEvent (line 178) of
+// services/billing/src/chargeable-events.ts log `{ error: err?.message }` with the read INSIDE the logger call's arguments, unguarded.
+// A thrown value whose read throws (a revoked Proxy, an Error whose message getter throws) makes the catch itself throw: the line is
+// never logged, loadChargeEventsFromDb (the boot ready hook) REJECTS instead of resolving, and a hostile ensureTable failure
+// escapes into the outer catch of createChargeEvent so that the INSERT is skipped, where an ordinary Error from ensureTable is
+// logged and the INSERT still runs; an Error whose message is readable but not a string (a Symbol) is handed to the logger
+// uncoerced. The cells make the db stand-in reject one statement with such a value and assert the function resolves, the line
+// carries text (the constant when the value cannot be turned into text) and the INSERT is issued as for an ordinary Error. Harness:
+// the real module with ../db replaced by a plain stand-in (its query rejects the chosen statement with the value), the shared
+// tenant helpers by plain pass-through functions and the logger by a plain recording object (no database).
+const h = vi.hoisted(() => ({
+  toThrow: undefined as unknown,
+  failOn: undefined as RegExp | undefined,
+  sqls: [] as string[],
+  logged: [] as { level: string; message: string; meta: Record<string, unknown> | undefined }[],
+}));
+
+vi.mock('../db', () => ({
+  isDbAvailable: () => true,
+  query: (sql: string) => {
+    h.sqls.push(String(sql));
+    if (h.failOn && h.failOn.test(String(sql))) return Promise.reject(h.toThrow);
+    return Promise.resolve({ rows: [{ cnt: '0' }] });
+  },
+}));
+
+vi.mock('@secuura/shared', () => ({
+  runWithTenantId: (_tenant: unknown, fn: () => unknown) => fn(),
+  runWithPlatformScope: (fn: () => unknown) => fn(),
+}));
+
+vi.mock('../utils/logger', () => {
+  const rec = (level: string) => (message: string, meta?: Record<string, unknown>) => {
+    h.logged.push({ level, message, meta });
+  };
+  return { logger: { debug: rec('debug'), info: rec('info'), warn: rec('warn'), error: rec('error') } };
+});
+
+type Ce = typeof import('../chargeable-events');
+const TENANT = 'a0000000-0000-4000-8000-000000000001';
+const ENSURE = 'Failed to ensure billing_charge_events table';
+const VERIFY = 'Failed to verify billing_charge_events table';
+const INSERT = 'DB insert failed for charge event';
+
+beforeEach(() => {
+  h.toThrow = undefined;
+  h.failOn = undefined;
+  h.sqls.length = 0;
+  h.logged.length = 0;
+});
+
+async function freshCe(): Promise<Ce> {
+  vi.resetModules();
+  return import('../chargeable-events');
+}
+async function create(failOn: RegExp, value: unknown): Promise<{ ok: boolean; inserted: boolean }> {
+  h.failOn = failOn;
+  h.toThrow = value;
+  const ce = await freshCe();
+  try {
+    await ce.createChargeEvent('certification_sign', 'cert_1', 'user_1', TENANT);
+    return { ok: true, inserted: h.sqls.some((s) => /INSERT INTO billing_charge_events/.test(s)) };
+  } catch {
+    return { ok: false, inserted: false };
+  }
+}
+async function verify(value: unknown): Promise<{ ok: boolean }> {
+  h.failOn = /COUNT\(\*\)/;
+  h.toThrow = value;
+  const ce = await freshCe();
+  try {
+    await ce.loadChargeEventsFromDb();
+    return { ok: true };
+  } catch {
+    return { ok: false };
+  }
+}
+const LINES = (message: string) => h.logged.filter((l) => l.message === message);
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
+describe('KS-1868 the charge-event table and insert catches log text for a hostile thrown value', () => {
+  it('control ks1868 C1: an ordinary Error from the table bootstrap is logged with its message and the INSERT still runs', async () => {
+    expect(await create(/CREATE TABLE/, new Error('ddl failed'))).toEqual({ ok: true, inserted: true });
+    expect(LINES(ENSURE)).toHaveLength(1);
+    expect(reasonOf(LINES(ENSURE)[0])).toBe('ddl failed');
+  });
+  it('control ks1868 C2: an ordinary Error from the table verify query is logged with its message and the call resolves', async () => {
+    expect(await verify(new Error('count failed'))).toEqual({ ok: true });
+    expect(LINES(VERIFY)).toHaveLength(1);
+    expect(reasonOf(LINES(VERIFY)[0])).toBe('count failed');
+  });
+  it('control ks1868 C3: an ordinary Error from the INSERT is logged with its message and the event is still returned', async () => {
+    expect(await create(/INSERT INTO billing_charge_events/, new Error('insert failed'))).toEqual({ ok: true, inserted: true });
+    expect(LINES(INSERT)).toHaveLength(1);
+    expect(reasonOf(LINES(INSERT)[0])).toBe('insert failed');
+  });
+  it('RED ks1868 R1: a table bootstrap failure that is a revoked Proxy is logged as text and the INSERT still runs, as for an ordinary Error', async () => {
+    expect(await create(/CREATE TABLE/, revokedProxy())).toEqual({ ok: true, inserted: true });
+    expect(LINES(ENSURE)).toHaveLength(1);
+    expect(reasonOf(LINES(ENSURE)[0])).toBe('unreadable thrown value');
+  });
+  it('RED ks1868 R2: a table bootstrap failure that is an Error whose message is a Symbol is logged as text and the INSERT still runs, as for an ordinary Error', async () => {
+    expect(await create(/CREATE TABLE/, withMessage(Symbol('ks1868')))).toEqual({ ok: true, inserted: true });
+    expect(LINES(ENSURE)).toHaveLength(1);
+    expect(reasonOf(LINES(ENSURE)[0])).toBe('Symbol(ks1868)');
+  });
+  it('RED ks1868 R3: a table verify failure that is an Error whose message getter throws resolves and is logged as text, as for an ordinary Error', async () => {
+    expect(await verify(getterThrows())).toEqual({ ok: true });
+    expect(LINES(VERIFY)).toHaveLength(1);
+    expect(reasonOf(LINES(VERIFY)[0])).toBe('unreadable thrown value');
+  });
+  it('RED ks1868 R4: a table verify failure that is a revoked Proxy resolves and is logged as text, as for an ordinary Error', async () => {
+    expect(await verify(revokedProxy())).toEqual({ ok: true });
+    expect(LINES(VERIFY)).toHaveLength(1);
+    expect(reasonOf(LINES(VERIFY)[0])).toBe('unreadable thrown value');
+  });
+  it('RED ks1868 R5: an INSERT failure that is a revoked Proxy is logged as text and the event is still returned, as for an ordinary Error', async () => {
+    expect(await create(/INSERT INTO billing_charge_events/, revokedProxy())).toEqual({ ok: true, inserted: true });
+    expect(LINES(INSERT)).toHaveLength(1);
+    expect(reasonOf(LINES(INSERT)[0])).toBe('unreadable thrown value');
+  });
+  it('RED ks1868 R6: an INSERT failure that is an Error whose message is a Symbol is logged as text and the event is still returned, as for an ordinary Error', async () => {
+    expect(await create(/INSERT INTO billing_charge_events/, withMessage(Symbol('ks1868')))).toEqual({ ok: true, inserted: true });
+    expect(LINES(INSERT)).toHaveLength(1);
+    expect(reasonOf(LINES(INSERT)[0])).toBe('Symbol(ks1868)');
+  });
+});
```
