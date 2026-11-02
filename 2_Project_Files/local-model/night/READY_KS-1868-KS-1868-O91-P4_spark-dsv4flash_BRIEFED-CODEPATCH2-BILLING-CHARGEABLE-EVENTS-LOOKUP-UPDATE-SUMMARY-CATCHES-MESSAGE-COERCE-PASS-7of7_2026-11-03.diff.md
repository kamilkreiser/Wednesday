# READY — KS-1868-KS-1868-O91-P4 (spark-dsv4flash, briefed, code_patch2, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o91_p4_billing_chargeable_events_lookup_update_and_summary_catches_guard_message/out.md.checker/patch.diff`** (from `ls` at 07:20 2026-11-03; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o91_p4_billing_chargeable_events_lookup_update_and_summary_catches_guard_message/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o91_p4_billing_chargeable_events_lookup_update_and_summary_catches_guard_message/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o91_p4_billing_chargeable_events_lookup_update_and_summary_catches_guard_message/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o91_p4_billing_chargeable_events_lookup_update_and_summary_catches_guard_message-control/out.md.checker/patch.diff` rc 0, Wednesday).

**Held 07:20 2026-11-03 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o91_p4_billing_chargeable_events_lookup_update_and_summary_catches_guard_message/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `26955bf1b828113fcfe29b6bd6e371dbe28b5360`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/services/billing/src/chargeable-events.ts } + { Blockchain/Dev/services/billing/src/__tests__/ks1868-billing-chargeable-events-lookup-update-summary-catches-unreadable-throw.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/billing/src/chargeable-events.ts` (product) and `Blockchain/Dev/services/billing/src/__tests__/ks1868-billing-chargeable-events-lookup-update-summary-catches-unreadable-throw.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
24	3	Blockchain/Dev/services/billing/src/chargeable-events.ts
165	0	Blockchain/Dev/services/billing/src/__tests__/ks1868-billing-chargeable-events-lookup-update-summary-catches-unreadable-throw.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (24 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: chargeable-events.ts`
- CODE_PATCH2 (rung 3, 1 product files + 1 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/services/billing/src/chargeable-events.ts`; test(s): `Blockchain/Dev/services/billing/src/__tests__/ks1868-billing-chargeable-events-lookup-update-summary-catches-unreadable-throw.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/services/billing/src/chargeable-events.ts 24 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/billing/src/__tests__/ks1868-billing-chargeable-events-lookup-update-summary-catches-unreadable-throw.test.ts 165 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/billing/src/chargeable-events.ts` (hunks=3, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/billing/src/__tests__/ks1868-billing-chargeable-events-lookup-update-summary-catches-unreadable-throw.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (6 failed / 9 run; controls green; assertion reds)` [red_first.json: failed=6 of total=9; red cell(s): ['KS-1868 the charge-event lookup, update and usage-summary catches log text for a hostile thrown value RED ks1868 R1: a lookup failure that is a revoked Proxy is logged as text and processChargeEvent answers null, as for an ordinary Error', 'KS-1868 the charge-event lookup, update and usage-summary catches log text for a hostile thrown value RED ks1868 R2: a lookup failure that is an Error whose message is a Symbol is logged as text and processChargeEvent answers null, as for an ordinary Error', 'KS-1868 the charge-event lookup, update and usage-summary catches log text for a hostile thrown value RED ks1868 R3: an update failure that is a revoked Proxy is logged as text and processChargeEvent answers the event, as for an ordinary Error', 'KS-1868 the charge-event lookup, update and usage-summary catches log text for a hostile thrown value RED ks1868 R4: an update failure that is an Error whose message getter throws is logged as text and processChargeEvent answers the event, as for an ordinary Error', 'KS-1868 the charge-event lookup, update and usage-summary catches log text for a hostile thrown value RED ks1868 R5: a usage query failure that is a revoked Proxy is logged as text and getUsageSummary answers its empty defaults, as for an ordinary Error', 'KS-1868 the charge-event lookup, update and usage-summary catches log text for a hostile thrown value RED ks1868 R6: a usage query failure that is an Error whose message is a Symbol is logged as text and getUsageSummary answers its empty defaults, as for an ordinary Error']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 1 product section(s) (9 passed / 9 run)` [green_after.json: failed=0 of total=9, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=368 failed=0 | after: total=377 failed=0` · `NEW reds: []` [baseline_suite.json total=368 failed=0; after_suite.json total=377 failed=0]
- A6 [verbatim]: `PASS A6 whole services/billing suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/billing: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 products=1 tests=1 red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/billing/src/chargeable-events.ts` (+24/-3 per numstat.out) and the test file `Blockchain/Dev/services/billing/src/__tests__/ks1868-billing-chargeable-events-lookup-update-summary-catches-unreadable-throw.test.ts` (+165/-0); 2 files in all (code_patch2: products Blockchain/Dev/services/billing/src/chargeable-events.ts). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `26955bf1b828113fcfe29b6bd6e371dbe28b5360` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o91_p4_billing_chargeable_events_lookup_update_and_summary_catches_guard_message/input.json`. Brief (given by --brief; its `# ` heading names KS-1868): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1868_o91_p4_billing_chargeable_events_lookup_update_and_summary_catches_guard_message/KS-1868.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o91_p4_billing_chargeable_events_lookup_update_and_summary_catches_guard_message/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/billing/src/chargeable-events.ts b/Blockchain/Dev/services/billing/src/chargeable-events.ts
--- a/Blockchain/Dev/services/billing/src/chargeable-events.ts
+++ b/Blockchain/Dev/services/billing/src/chargeable-events.ts
@@ -235,6 +235,13 @@
       };
     }
   } catch (err: any) {
-    logger.warn('DB lookup failed for charge event', { error: err?.message, eventId });
+    let reason: string | null | undefined;
+    try {
+      const m = err?.message;
+      reason = m === undefined || m === null ? m : String(m);
+    } catch {
+      reason = 'unreadable thrown value';
+    }
+    logger.warn('DB lookup failed for charge event', { error: reason, eventId });
     return null;
   }
@@ -262,5 +269,12 @@
       [status, JSON.stringify(event.metadata ?? {}), eventId, tenantId]
     ));
   } catch (err: any) {
-    logger.warn('DB update failed for charge event', { error: err?.message, eventId });
+    let reason: string | null | undefined;
+    try {
+      const m = err?.message;
+      reason = m === undefined || m === null ? m : String(m);
+    } catch {
+      reason = 'unreadable thrown value';
+    }
+    logger.warn('DB update failed for charge event', { error: reason, eventId });
   }
@@ -415,7 +429,14 @@
       discountApplied: applicableDiscount?.discountPercent || 0,
     };
   } catch (err: any) {
-    logger.warn('DB query failed for usage summary — returning empty defaults', { error: err?.message });
+    let reason: string | null | undefined;
+    try {
+      const m = err?.message;
+      reason = m === undefined || m === null ? m : String(m);
+    } catch {
+      reason = 'unreadable thrown value';
+    }
+    logger.warn('DB query failed for usage summary — returning empty defaults', { error: reason });
     return {
       period: { start: startDate, end: endDate },
       totalEvents: 0,
diff --git a/Blockchain/Dev/services/billing/src/__tests__/ks1868-billing-chargeable-events-lookup-update-summary-catches-unreadable-throw.test.ts b/Blockchain/Dev/services/billing/src/__tests__/ks1868-billing-chargeable-events-lookup-update-summary-catches-unreadable-throw.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/billing/src/__tests__/ks1868-billing-chargeable-events-lookup-update-summary-catches-unreadable-throw.test.ts
@@ -0,0 +1,165 @@
+import { describe, it, expect, beforeEach, vi } from 'vitest';
+
+// KS-1868 (operator 91 screen, billing chargeable events): the lookup catch (line 238) and the update catch (line 265) of
+// processChargeEvent and the query catch (line 418) of getUsageSummary in services/billing/src/chargeable-events.ts log
+// `{ error: err?.message }` with the read INSIDE the logger call's arguments, unguarded. A thrown value whose read throws (a revoked
+// Proxy, an Error whose message getter throws) makes the catch itself throw: the warn line is never logged and the function
+// REJECTS where an ordinary Error makes processChargeEvent answer null (lookup), answer the event (update) and getUsageSummary answer
+// its empty defaults; an Error whose message is readable but not a string (a Symbol) is handed to the logger uncoerced. The cells
+// make the db stand-in reject one statement with such a value and assert the function resolves with the ordinary answer and the
+// line carries text (the constant when the value cannot be turned into text). Harness: the real module with ../db replaced by a plain
+// stand-in (its query answers the lookup with one pending event and rejects the chosen statement with the value), the shared tenant
+// helpers by plain pass-through functions and the logger by a plain recording object (no database).
+const h = vi.hoisted(() => ({
+  toThrow: undefined as unknown,
+  failOn: undefined as RegExp | undefined,
+  logged: [] as { level: string; message: string; meta: Record<string, unknown> | undefined }[],
+}));
+
+vi.mock('../db', () => ({
+  isDbAvailable: () => true,
+  query: (sql: string) => {
+    if (h.failOn && h.failOn.test(String(sql))) return Promise.reject(h.toThrow);
+    if (/SELECT id, event_type/.test(String(sql))) {
+      return Promise.resolve({
+        rows: [
+          {
+            id: 'ce_1',
+            event_type: 'certification_sign',
+            certification_id: 'cert_1',
+            initiated_by: 'user_1',
+            amount: '1',
+            currency: 'ADA',
+            status: 'pending',
+            metadata: {},
+            created_at: '2026-01-01T00:00:00.000Z',
+          },
+        ],
+      });
+    }
+    return Promise.resolve({ rows: [] });
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
+const LOOKUP = 'DB lookup failed for charge event';
+const UPDATE = 'DB update failed for charge event';
+const SUMMARY = 'DB query failed for usage summary — returning empty defaults';
+
+beforeEach(() => {
+  h.toThrow = undefined;
+  h.failOn = undefined;
+  h.logged.length = 0;
+});
+
+async function freshCe(): Promise<Ce> {
+  vi.resetModules();
+  return import('../chargeable-events');
+}
+async function process_(failOn: RegExp, value: unknown): Promise<{ ok: boolean; answer: string }> {
+  h.failOn = failOn;
+  h.toThrow = value;
+  const ce = await freshCe();
+  try {
+    const ev = await ce.processChargeEvent('ce_1', 'completed', TENANT);
+    return { ok: true, answer: ev === null ? 'null' : 'event:' + ev.status };
+  } catch {
+    return { ok: false, answer: '' };
+  }
+}
+async function summary(value: unknown): Promise<{ ok: boolean; answer: string }> {
+  h.failOn = /COUNT\(\*\)/;
+  h.toThrow = value;
+  const ce = await freshCe();
+  try {
+    const s = await ce.getUsageSummary('user_1', TENANT, new Date('2026-01-01T00:00:00.000Z'), new Date('2026-02-01T00:00:00.000Z'));
+    return { ok: true, answer: 'events:' + s.totalEvents };
+  } catch {
+    return { ok: false, answer: '' };
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
+const LOOKUP_SQL = /SELECT id, event_type/;
+const UPDATE_SQL = /UPDATE billing_charge_events/;
+
+describe('KS-1868 the charge-event lookup, update and usage-summary catches log text for a hostile thrown value', () => {
+  it('control ks1868 C1: an ordinary Error from the lookup is logged with its message and processChargeEvent answers null', async () => {
+    expect(await process_(LOOKUP_SQL, new Error('lookup failed'))).toEqual({ ok: true, answer: 'null' });
+    expect(LINES(LOOKUP)).toHaveLength(1);
+    expect(reasonOf(LINES(LOOKUP)[0])).toBe('lookup failed');
+  });
+  it('control ks1868 C2: an ordinary Error from the update is logged with its message and processChargeEvent answers the event', async () => {
+    expect(await process_(UPDATE_SQL, new Error('update failed'))).toEqual({ ok: true, answer: 'event:completed' });
+    expect(LINES(UPDATE)).toHaveLength(1);
+    expect(reasonOf(LINES(UPDATE)[0])).toBe('update failed');
+  });
+  it('control ks1868 C3: an ordinary Error from the usage query is logged with its message and getUsageSummary answers its empty defaults', async () => {
+    expect(await summary(new Error('query failed'))).toEqual({ ok: true, answer: 'events:0' });
+    expect(LINES(SUMMARY)).toHaveLength(1);
+    expect(reasonOf(LINES(SUMMARY)[0])).toBe('query failed');
+  });
+  it('RED ks1868 R1: a lookup failure that is a revoked Proxy is logged as text and processChargeEvent answers null, as for an ordinary Error', async () => {
+    expect(await process_(LOOKUP_SQL, revokedProxy())).toEqual({ ok: true, answer: 'null' });
+    expect(LINES(LOOKUP)).toHaveLength(1);
+    expect(reasonOf(LINES(LOOKUP)[0])).toBe('unreadable thrown value');
+  });
+  it('RED ks1868 R2: a lookup failure that is an Error whose message is a Symbol is logged as text and processChargeEvent answers null, as for an ordinary Error', async () => {
+    expect(await process_(LOOKUP_SQL, withMessage(Symbol('ks1868')))).toEqual({ ok: true, answer: 'null' });
+    expect(LINES(LOOKUP)).toHaveLength(1);
+    expect(reasonOf(LINES(LOOKUP)[0])).toBe('Symbol(ks1868)');
+  });
+  it('RED ks1868 R3: an update failure that is a revoked Proxy is logged as text and processChargeEvent answers the event, as for an ordinary Error', async () => {
+    expect(await process_(UPDATE_SQL, revokedProxy())).toEqual({ ok: true, answer: 'event:completed' });
+    expect(LINES(UPDATE)).toHaveLength(1);
+    expect(reasonOf(LINES(UPDATE)[0])).toBe('unreadable thrown value');
+  });
+  it('RED ks1868 R4: an update failure that is an Error whose message getter throws is logged as text and processChargeEvent answers the event, as for an ordinary Error', async () => {
+    expect(await process_(UPDATE_SQL, getterThrows())).toEqual({ ok: true, answer: 'event:completed' });
+    expect(LINES(UPDATE)).toHaveLength(1);
+    expect(reasonOf(LINES(UPDATE)[0])).toBe('unreadable thrown value');
+  });
+  it('RED ks1868 R5: a usage query failure that is a revoked Proxy is logged as text and getUsageSummary answers its empty defaults, as for an ordinary Error', async () => {
+    expect(await summary(revokedProxy())).toEqual({ ok: true, answer: 'events:0' });
+    expect(LINES(SUMMARY)).toHaveLength(1);
+    expect(reasonOf(LINES(SUMMARY)[0])).toBe('unreadable thrown value');
+  });
+  it('RED ks1868 R6: a usage query failure that is an Error whose message is a Symbol is logged as text and getUsageSummary answers its empty defaults, as for an ordinary Error', async () => {
+    expect(await summary(withMessage(Symbol('ks1868')))).toEqual({ ok: true, answer: 'events:0' });
+    expect(LINES(SUMMARY)).toHaveLength(1);
+    expect(reasonOf(LINES(SUMMARY)[0])).toBe('Symbol(ks1868)');
+  });
+});
```
