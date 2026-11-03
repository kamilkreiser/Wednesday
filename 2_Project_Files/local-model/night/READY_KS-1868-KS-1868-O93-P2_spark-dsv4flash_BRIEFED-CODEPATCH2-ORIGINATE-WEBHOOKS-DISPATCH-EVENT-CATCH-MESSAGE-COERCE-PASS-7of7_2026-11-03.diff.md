# READY — KS-1868-KS-1868-O93-P2 (spark-dsv4flash, briefed, code_patch2, jest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o93_p2_originate_webhooks_dispatch_event_catch_guard_message/out.md.checker/patch.diff`** (from `ls` at 09:55 2026-11-03; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o93_p2_originate_webhooks_dispatch_event_catch_guard_message/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o93_p2_originate_webhooks_dispatch_event_catch_guard_message/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o93_p2_originate_webhooks_dispatch_event_catch_guard_message/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o93_p2_originate_webhooks_dispatch_event_catch_guard_message-control/out.md.checker/patch.diff` rc 0, Wednesday).

**Held 09:55 2026-11-03 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o93_p2_originate_webhooks_dispatch_event_catch_guard_message/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `66cbe4e52d5afadc9d13ca141200026cc68d5095`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/services/originate/src/routes/webhooks.ts } + { Blockchain/Dev/services/originate/src/__tests__/ks1868-originate-webhooks-dispatch-event-catch-unreadable-throw.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/originate/src/routes/webhooks.ts` (product) and `Blockchain/Dev/services/originate/src/__tests__/ks1868-originate-webhooks-dispatch-event-catch-unreadable-throw.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
8	1	Blockchain/Dev/services/originate/src/routes/webhooks.ts
106	0	Blockchain/Dev/services/originate/src/__tests__/ks1868-originate-webhooks-dispatch-event-catch-unreadable-throw.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (8 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: webhooks.ts`
- CODE_PATCH2 (rung 3, 1 product files + 1 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/services/originate/src/routes/webhooks.ts`; test(s): `Blockchain/Dev/services/originate/src/__tests__/ks1868-originate-webhooks-dispatch-event-catch-unreadable-throw.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/services/originate/src/routes/webhooks.ts 8 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/originate/src/__tests__/ks1868-originate-webhooks-dispatch-event-catch-unreadable-throw.test.ts 106 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/originate/src/routes/webhooks.ts` (hunks=1, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/originate/src/__tests__/ks1868-originate-webhooks-dispatch-event-catch-unreadable-throw.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (3 failed / 5 run; controls green; assertion reds)` [red_first.json: failed=3 of total=5; red cell(s): ['KS-1868 the dispatchEvent catch resolves 0 and logs text for a hostile thrown value RED ks1868 R1: a revoked Proxy from the delivery request is logged as text and dispatchEvent resolves 0, as for an ordinary Error', 'KS-1868 the dispatchEvent catch resolves 0 and logs text for a hostile thrown value RED ks1868 R2: an Error whose message is a Symbol from the delivery request is logged as text and dispatchEvent resolves 0, as for an ordinary Error', 'KS-1868 the dispatchEvent catch resolves 0 and logs text for a hostile thrown value RED ks1868 R3: an Error whose message getter throws from the delivery request is logged as text and dispatchEvent resolves 0, as for an ordinary Error']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 1 product section(s) (5 passed / 5 run)` [green_after.json: failed=0 of total=5, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=2375 failed=11 | after: total=2380 failed=11` · `NEW reds: []` [baseline_suite.json total=2375 failed=11; after_suite.json total=2380 failed=11]
- A6 [verbatim]: `PASS A6 whole services/originate suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/originate: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 products=1 tests=1 red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/originate/src/routes/webhooks.ts` (+8/-1 per numstat.out) and the test file `Blockchain/Dev/services/originate/src/__tests__/ks1868-originate-webhooks-dispatch-event-catch-unreadable-throw.test.ts` (+106/-0); 2 files in all (code_patch2: products Blockchain/Dev/services/originate/src/routes/webhooks.ts). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `66cbe4e52d5afadc9d13ca141200026cc68d5095` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o93_p2_originate_webhooks_dispatch_event_catch_guard_message/input.json`. Brief (given by --brief; its `# ` heading names KS-1868): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1868_o93_p2_originate_webhooks_dispatch_event_catch_guard_message/KS-1868.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o93_p2_originate_webhooks_dispatch_event_catch_guard_message/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/originate/src/routes/webhooks.ts b/Blockchain/Dev/services/originate/src/routes/webhooks.ts
--- a/Blockchain/Dev/services/originate/src/routes/webhooks.ts
+++ b/Blockchain/Dev/services/originate/src/routes/webhooks.ts
@@ -550,7 +550,14 @@
     logger.info('Webhook dispatch', { eventType, total: webhooks.length, delivered });
     return delivered;
   } catch (err: any) {
-    logger.warn('Webhook dispatch failed', { eventType, error: err.message });
+    let reason: string | null | undefined;
+    try {
+      const m = err.message;
+      reason = m === undefined || m === null ? m : String(m);
+    } catch {
+      reason = 'unreadable thrown value';
+    }
+    logger.warn('Webhook dispatch failed', { eventType, error: reason });
     return 0;
   }
 }
diff --git a/Blockchain/Dev/services/originate/src/__tests__/ks1868-originate-webhooks-dispatch-event-catch-unreadable-throw.test.ts b/Blockchain/Dev/services/originate/src/__tests__/ks1868-originate-webhooks-dispatch-event-catch-unreadable-throw.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/originate/src/__tests__/ks1868-originate-webhooks-dispatch-event-catch-unreadable-throw.test.ts
@@ -0,0 +1,106 @@
+// KS-1868 (operator 93 screen, originate webhooks): the outer catch of dispatchEvent (line 553) of services/originate/src/routes/webhooks.ts reads
+// `err.message` inside the logger call's arguments, unguarded. A thrown value whose read throws (a revoked Proxy, an Error whose message getter throws)
+// makes the catch throw, so dispatchEvent REJECTS where an ordinary Error is logged and it resolves 0 (the callers fire it as a best-effort notification);
+// an Error whose message is readable but not a string (a Symbol) is handed to the logger uncoerced and dropped from the JSON line. The cells make the
+// delivery request reject with such a value (the stand-in of the outbound request, which dispatchEvent awaits inside its try) and assert dispatchEvent
+// resolves 0 and the line carries text (the constant when the value cannot be turned into text). Harness: the ks914 deliverWebhook suite (same mocks);
+// the database stand-in answers one active webhook row; the outbound request stand-in is a plain function, not jest.fn(): a spy inspects what it
+// rejects with and could itself fail on a revoked Proxy before the code under test saw it. Nothing is written and nothing is sent.
+const mockState: { toThrow: unknown; warned: unknown[][] } = { toThrow: undefined, warned: [] };
+
+jest.mock('../db', () => ({ prisma: { $queryRaw: jest.fn(), $executeRaw: jest.fn() } }));
+jest.mock('../middleware/auth', () => ({
+  authenticate: () => (_req: unknown, _res: unknown, next: () => void) => next(),
+}));
+jest.mock('../utils/logger', () => ({
+  logger: {
+    info: () => undefined,
+    debug: () => undefined,
+    error: () => undefined,
+    warn: (...args: unknown[]) => {
+      mockState.warned.push(args);
+    },
+  },
+}));
+jest.mock('@secuura/shared', () =>
+  require('./helpers/sharedModuleMock').makeSharedMock({
+    encryptField: (v: unknown) => v,
+    decryptField: (v: unknown) => v,
+    runWithTenantId: (_t: unknown, fn: () => unknown) => fn(),
+    assertSafeOutboundUrl: jest.fn(),
+    safeOutboundRequest: (..._args: unknown[]) => Promise.reject(mockState.toThrow),
+  }),
+);
+
+import { dispatchEvent } from '../routes/webhooks';
+
+const db = {
+  $queryRaw: (..._args: unknown[]) =>
+    Promise.resolve([{ id: '11111111-2222-4333-8444-555555555555', url: 'https://subscriber.example/hook', secret_v2: null }]),
+  $executeRaw: (..._args: unknown[]) => Promise.resolve(1),
+};
+
+const FAILED = 'Webhook dispatch failed';
+const LINE = (): Record<string, unknown>[] =>
+  mockState.warned.filter((a) => a[0] === FAILED).map((a) => a[1] as Record<string, unknown>);
+/** The logged `error` field as a string; the type name when it is not one (a hostile value never reaches an assertion). */
+const reasonOf = (o: Record<string, unknown> | undefined): string => (typeof o?.error === 'string' ? (o.error as string) : '<' + typeof o?.error + '>');
+
+async function dispatch(value: unknown): Promise<{ threw: boolean; delivered: number | undefined }> {
+  mockState.toThrow = value;
+  try {
+    return { threw: false, delivered: await dispatchEvent('document.created', { id: 'doc-1' }, db) };
+  } catch {
+    return { threw: true, delivered: undefined };
+  }
+}
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
+describe('KS-1868 the dispatchEvent catch resolves 0 and logs text for a hostile thrown value', () => {
+  beforeEach(() => {
+    mockState.toThrow = undefined;
+    mockState.warned.length = 0;
+  });
+
+  it('control ks1868 C1: an ordinary Error from the delivery request is logged with its message and dispatchEvent resolves 0', async () => {
+    expect(await dispatch(new Error('send boom'))).toEqual({ threw: false, delivered: 0 });
+    expect(LINE()).toHaveLength(1);
+    expect(reasonOf(LINE()[0])).toBe('send boom');
+    expect(LINE()[0].eventType).toBe('document.created');
+  });
+  it('control ks1868 C2: a thrown plain string is logged without a message and dispatchEvent resolves 0', async () => {
+    expect(await dispatch('plain boom')).toEqual({ threw: false, delivered: 0 });
+    expect(LINE()).toHaveLength(1);
+    expect(reasonOf(LINE()[0])).toBe('<undefined>');
+  });
+  it('RED ks1868 R1: a revoked Proxy from the delivery request is logged as text and dispatchEvent resolves 0, as for an ordinary Error', async () => {
+    expect(await dispatch(revokedProxy())).toEqual({ threw: false, delivered: 0 });
+    expect(LINE()).toHaveLength(1);
+    expect(reasonOf(LINE()[0])).toBe('unreadable thrown value');
+  });
+  it('RED ks1868 R2: an Error whose message is a Symbol from the delivery request is logged as text and dispatchEvent resolves 0, as for an ordinary Error', async () => {
+    expect(await dispatch(withMessage(Symbol('ks1868')))).toEqual({ threw: false, delivered: 0 });
+    expect(LINE()).toHaveLength(1);
+    expect(reasonOf(LINE()[0])).toBe('Symbol(ks1868)');
+  });
+  it('RED ks1868 R3: an Error whose message getter throws from the delivery request is logged as text and dispatchEvent resolves 0, as for an ordinary Error', async () => {
+    expect(await dispatch(getterThrows())).toEqual({ threw: false, delivered: 0 });
+    expect(LINE()).toHaveLength(1);
+    expect(reasonOf(LINE()[0])).toBe('unreadable thrown value');
+  });
+});
```
