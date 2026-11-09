# READY — KS-2094-KS-2094-O121-P1 (Spark (DeepSeek V4 Flash), briefed, code_patch2, jest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-09_ks_2094_o121_p1_originate_publish_event_logs_a_failed_publish/out.md.checker/patch.diff`** (from `ls` at 22:56 2026-11-09; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-09_ks_2094_o121_p1_originate_publish_event_logs_a_failed_publish/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-09_ks_2094_o121_p1_originate_publish_event_logs_a_failed_publish/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-09_ks_2094_o121_p1_originate_publish_event_logs_a_failed_publish/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-09_ks_2094_o121_p1_originate_publish_event_logs_a_failed_publish-control-r3/out.md.checker/patch.diff` rc 0, Wednesday).

**Held 22:56 2026-11-09 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-09_ks_2094_o121_p1_originate_publish_event_logs_a_failed_publish/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `d0b4825cc24493213f82b609670a4a0fa521a4b9`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/services/originate/src/events.ts } + { Blockchain/Dev/services/originate/src/__tests__/ks2094-publish-event-logs-a-failed-publish-instead-of-swallowing-it.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/originate/src/events.ts` (product) and `Blockchain/Dev/services/originate/src/__tests__/ks2094-publish-event-logs-a-failed-publish-instead-of-swallowing-it.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
5	2	Blockchain/Dev/services/originate/src/events.ts
109	0	Blockchain/Dev/services/originate/src/__tests__/ks2094-publish-event-logs-a-failed-publish-instead-of-swallowing-it.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (5 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: events.ts`
- CODE_PATCH2 (rung 3, 1 product files + 1 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/services/originate/src/events.ts`; test(s): `Blockchain/Dev/services/originate/src/__tests__/ks2094-publish-event-logs-a-failed-publish-instead-of-swallowing-it.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/services/originate/src/events.ts 5 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/originate/src/__tests__/ks2094-publish-event-logs-a-failed-publish-instead-of-swallowing-it.test.ts 109 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/originate/src/events.ts` (hunks=1, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/originate/src/__tests__/ks2094-publish-event-logs-a-failed-publish-instead-of-swallowing-it.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (3 failed / 5 run; controls green; assertion reds)` [red_first.json: failed=3 of total=5; red cell(s): ['KS-2094 publishEvent logs a failed publish instead of swallowing it RED ks2094 R1: a rejected xadd still resolves publishEvent and logs one warning naming the type and the message', 'KS-2094 publishEvent logs a failed publish instead of swallowing it RED ks2094 R2: a refused connect still resolves publishEvent and logs one warning naming the type and the message', 'KS-2094 publishEvent logs a failed publish instead of swallowing it RED ks2094 R3: a revoked Proxy thrown by xadd still resolves publishEvent and is logged as a constant reason']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 1 product section(s) (5 passed / 5 run)` [green_after.json: failed=0 of total=5, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=2592 failed=11 | after: total=2597 failed=11` · `NEW reds: []` [baseline_suite.json total=2592 failed=11; after_suite.json total=2597 failed=11]
- A6 [verbatim]: `PASS A6 whole services/originate suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/originate: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 products=1 tests=1 red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/originate/src/events.ts` (+5/-2 per numstat.out) and the test file `Blockchain/Dev/services/originate/src/__tests__/ks2094-publish-event-logs-a-failed-publish-instead-of-swallowing-it.test.ts` (+109/-0); 2 files in all (code_patch2: products Blockchain/Dev/services/originate/src/events.ts). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `d0b4825cc24493213f82b609670a4a0fa521a4b9` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-09_ks_2094_o121_p1_originate_publish_event_logs_a_failed_publish/input.json`. brief NOT LOCATED under night/briefs/ (no claim made). Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-09_ks_2094_o121_p1_originate_publish_event_logs_a_failed_publish/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/originate/src/events.ts b/Blockchain/Dev/services/originate/src/events.ts
--- a/Blockchain/Dev/services/originate/src/events.ts
+++ b/Blockchain/Dev/services/originate/src/events.ts
@@ -141,6 +141,9 @@
       JSON.stringify(event),
     );
-  } catch {
-    // Fire-and-forget — never let event publishing break the service
+  } catch (err: any) {
+    // Fire-and-forget — never let event publishing break the service. KS-2094: but a failed publish is logged, not silent.
+    let reason: string;
+    try { reason = err instanceof Error ? err.message : String(err); } catch { reason = 'unreadable thrown value'; }
+    logger.warn('Failed to publish event', { type, error: reason });
   }
 }
diff --git a/Blockchain/Dev/services/originate/src/__tests__/ks2094-publish-event-logs-a-failed-publish-instead-of-swallowing-it.test.ts b/Blockchain/Dev/services/originate/src/__tests__/ks2094-publish-event-logs-a-failed-publish-instead-of-swallowing-it.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/originate/src/__tests__/ks2094-publish-event-logs-a-failed-publish-instead-of-swallowing-it.test.ts
@@ -0,0 +1,109 @@
+// KS-2094: originate's publishEvent (src/events.ts) ended in an empty catch, so a Redis failure while publishing
+// (a refused connect, a rejected xadd) was silent: user.erased never reached its stream and nothing was logged. The catch
+// now logs one warning that names the event type and the reason as text, and publishEvent still never throws (its contract:
+// "never let event publishing break the service"). The reason is read as originate's other catches read a thrown value (an Error's
+// message, else String(err)), so a thrown value whose read throws is logged as a constant. Harness: the real module with ioredis replaced by a plain stand-in class
+// and the logger by a plain recording object (no Redis, no network).
+// KS-1989: with no import or export this file is a global script (TS2451 if another global script declares the same names). The empty export makes it a module.
+export {};
+const mockH: {
+  xaddFailure: undefined | { value: unknown };
+  connectFailure: undefined | { value: unknown };
+  xadds: unknown[][];
+  logs: { level: string; message: string; meta: Record<string, unknown> | undefined }[];
+} = { xaddFailure: undefined, connectFailure: undefined, xadds: [], logs: [] };
+
+jest.mock('ioredis', () => ({
+  __esModule: true,
+  default: function RedisMock() {
+    return {
+      status: 'wait',
+      on: () => undefined,
+      connect: async () => {
+        if (mockH.connectFailure) throw mockH.connectFailure.value;
+      },
+      disconnect: () => undefined,
+      xadd: async (...args: unknown[]) => {
+        if (mockH.xaddFailure) throw mockH.xaddFailure.value;
+        mockH.xadds.push(args);
+        return '1-0';
+      },
+    };
+  },
+}));
+jest.mock('../utils/logger', () => {
+  const rec = (level: string) => (message: string, meta?: Record<string, unknown>) => {
+    mockH.logs.push({ level, message, meta });
+  };
+  return { logger: { debug: rec('debug'), info: rec('info'), warn: rec('warn'), error: rec('error') } };
+});
+
+type Ev = typeof import('../events');
+beforeEach(() => {
+  mockH.xaddFailure = undefined;
+  mockH.connectFailure = undefined;
+  mockH.xadds.length = 0;
+  mockH.logs.length = 0;
+});
+
+function freshEvents(): Ev {
+  jest.resetModules();
+  // eslint-disable-next-line @typescript-eslint/no-require-imports
+  const ev = require('../events') as Ev;
+  ev.initEventBus('redis://localhost:6379');
+  return ev;
+}
+const PUBLISH = 'Failed to publish event';
+const LINE = (message: string): { level: string; message: string; meta: Record<string, unknown> | undefined }[] =>
+  mockH.logs.filter((l) => l.message === message);
+/** The logged field as a string; the type name when it is not one (a hostile value never reaches an assertion). */
+const fieldOf = (l: { meta: Record<string, unknown> | undefined } | undefined, k: string): string =>
+  typeof l?.meta?.[k] === 'string' ? (l!.meta![k] as string) : '<' + typeof l?.meta?.[k] + '>';
+
+const revokedProxy = (): unknown => {
+  const rp = Proxy.revocable({}, {});
+  rp.revoke();
+  return rp.proxy;
+};
+
+describe('KS-2094 publishEvent logs a failed publish instead of swallowing it', () => {
+  it('control ks2094 C1: a successful publish writes one stream entry and logs no publish failure', async () => {
+    const ev = freshEvents();
+    await expect(ev.publishEvent(ev.EventTypes.USER_ERASED, { userId: 'u1' })).resolves.toBeUndefined();
+    expect(mockH.xadds).toHaveLength(1);
+    expect(LINE(PUBLISH)).toHaveLength(0);
+  });
+  it('control ks2094 C2: with no Redis client publishEvent returns at once, writes nothing and logs no publish failure', async () => {
+    jest.resetModules();
+    // eslint-disable-next-line @typescript-eslint/no-require-imports
+    const ev = require('../events') as Ev;
+    await expect(ev.publishEvent(ev.EventTypes.USER_ERASED, { userId: 'u1' })).resolves.toBeUndefined();
+    expect(mockH.xadds).toHaveLength(0);
+    expect(LINE(PUBLISH)).toHaveLength(0);
+  });
+  it('RED ks2094 R1: a rejected xadd still resolves publishEvent and logs one warning naming the type and the message', async () => {
+    mockH.xaddFailure = { value: new Error('redis down') };
+    const ev = freshEvents();
+    await expect(ev.publishEvent(ev.EventTypes.USER_ERASED, { userId: 'u1' })).resolves.toBeUndefined();
+    expect(LINE(PUBLISH)).toHaveLength(1);
+    expect(LINE(PUBLISH)[0].level).toBe('warn');
+    expect(fieldOf(LINE(PUBLISH)[0], 'type')).toBe('user.erased');
+    expect(fieldOf(LINE(PUBLISH)[0], 'error')).toBe('redis down');
+  });
+  it('RED ks2094 R2: a refused connect still resolves publishEvent and logs one warning naming the type and the message', async () => {
+    mockH.connectFailure = { value: new Error('connect refused') };
+    const ev = freshEvents();
+    await expect(ev.publishEvent(ev.EventTypes.USER_ERASED, { userId: 'u1' })).resolves.toBeUndefined();
+    expect(mockH.xadds).toHaveLength(0);
+    expect(LINE(PUBLISH)).toHaveLength(1);
+    expect(fieldOf(LINE(PUBLISH)[0], 'error')).toBe('connect refused');
+  });
+  it('RED ks2094 R3: a revoked Proxy thrown by xadd still resolves publishEvent and is logged as a constant reason', async () => {
+    mockH.xaddFailure = { value: revokedProxy() };
+    const ev = freshEvents();
+    await expect(ev.publishEvent(ev.EventTypes.AUDIT_LOG, { n: 1 })).resolves.toBeUndefined();
+    expect(LINE(PUBLISH)).toHaveLength(1);
+    expect(fieldOf(LINE(PUBLISH)[0], 'type')).toBe('audit.log');
+    expect(fieldOf(LINE(PUBLISH)[0], 'error')).toBe('unreadable thrown value');
+  });
+});
```
