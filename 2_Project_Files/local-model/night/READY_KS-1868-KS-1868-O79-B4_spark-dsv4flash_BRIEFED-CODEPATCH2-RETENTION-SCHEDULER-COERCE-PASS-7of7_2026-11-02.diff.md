# READY — KS-1868-KS-1868-O79-B4 (spark-dsv4flash, briefed, code_patch2, jest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o79_b4_originate_retention_scheduler_guard_coerces_message/out.md.checker/patch.diff`** (from `ls` at 17:27 2026-11-02; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o79_b4_originate_retention_scheduler_guard_coerces_message/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o79_b4_originate_retention_scheduler_guard_coerces_message/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o79_b4_originate_retention_scheduler_guard_coerces_message/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o79_b4_originate_retention_scheduler_guard_coerces_message-control/out.md.checker/patch.diff` rc 0, Wednesday).

**Held 17:27 2026-11-02 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o79_b4_originate_retention_scheduler_guard_coerces_message/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `829233f1a388b943a9fd59c40e42332c27d9066b`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/services/originate/src/services/retentionScheduler.ts } + { Blockchain/Dev/services/originate/src/__tests__/ks1868-retention-scheduler-guard-coerces-message-o79b4.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/originate/src/services/retentionScheduler.ts` (product) and `Blockchain/Dev/services/originate/src/__tests__/ks1868-retention-scheduler-guard-coerces-message-o79b4.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
1	1	Blockchain/Dev/services/originate/src/services/retentionScheduler.ts
123	0	Blockchain/Dev/services/originate/src/__tests__/ks1868-retention-scheduler-guard-coerces-message-o79b4.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (1 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: retentionScheduler.ts`
- CODE_PATCH2 (rung 3, 1 product files + 1 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/services/originate/src/services/retentionScheduler.ts`; test(s): `Blockchain/Dev/services/originate/src/__tests__/ks1868-retention-scheduler-guard-coerces-message-o79b4.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/services/originate/src/services/retentionScheduler.ts 1 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/originate/src/__tests__/ks1868-retention-scheduler-guard-coerces-message-o79b4.test.ts 123 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/originate/src/services/retentionScheduler.ts` (hunks=1, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/originate/src/__tests__/ks1868-retention-scheduler-guard-coerces-message-o79b4.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (2 failed / 4 run; controls green; assertion reds)` [red_first.json: failed=2 of total=4; red cell(s): ['KS-1868 retention scheduler reads a hostile message safely RED ks1868 R1 runEnforcement: an Error whose message getter returns a revoked Proxy is logged as the constant reason through the real logger', 'KS-1868 retention scheduler reads a hostile message safely RED ks1868 R2 runEnforcement: an Error whose message getter returns an object with a throwing toJSON is logged as its string form through the real logger']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 1 product section(s) (4 passed / 4 run)` [green_after.json: failed=0 of total=4, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=2163 failed=0 | after: total=2167 failed=0` · `NEW reds: []` [baseline_suite.json total=2163 failed=0; after_suite.json total=2167 failed=0]
- A6 [verbatim]: `PASS A6 whole services/originate suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/originate: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 products=1 tests=1 red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/originate/src/services/retentionScheduler.ts` (+1/-1 per numstat.out) and the test file `Blockchain/Dev/services/originate/src/__tests__/ks1868-retention-scheduler-guard-coerces-message-o79b4.test.ts` (+123/-0); 2 files in all (code_patch2: products Blockchain/Dev/services/originate/src/services/retentionScheduler.ts). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `829233f1a388b943a9fd59c40e42332c27d9066b` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o79_b4_originate_retention_scheduler_guard_coerces_message/input.json`. Brief (given by --brief; its `# ` heading names KS-1868): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1868_o79_b4_originate_retention_scheduler_guard_coerces_message/KS-1868.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o79_b4_originate_retention_scheduler_guard_coerces_message/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/originate/src/services/retentionScheduler.ts b/Blockchain/Dev/services/originate/src/services/retentionScheduler.ts
--- a/Blockchain/Dev/services/originate/src/services/retentionScheduler.ts
+++ b/Blockchain/Dev/services/originate/src/services/retentionScheduler.ts
@@ -50,7 +50,7 @@
   } catch (err: any) {
     let reason: string;
     try {
-      reason = err instanceof Error ? err.message : String(err);
+      reason = String(err instanceof Error ? err.message : err);
     } catch {
       reason = 'unreadable thrown value';
     }
diff --git a/Blockchain/Dev/services/originate/src/__tests__/ks1868-retention-scheduler-guard-coerces-message-o79b4.test.ts b/Blockchain/Dev/services/originate/src/__tests__/ks1868-retention-scheduler-guard-coerces-message-o79b4.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/originate/src/__tests__/ks1868-retention-scheduler-guard-coerces-message-o79b4.test.ts
@@ -0,0 +1,123 @@
+// KS-1868 (originate services/retentionScheduler.ts, runEnforcement, follow-up of the guard PR 1923 merged): the scheduled data-retention run catches a failure of `enforceRetention()` and reads it as
+// `err instanceof Error ? err.message : String(err)` inside its own try, with the constant `unreadable thrown value` when that throws. That expression does not coerce `message`: for an Error whose `message` getter
+// RETURNS a hostile non-string (a revoked Proxy; an object whose toJSON throws) `reason` is that object, and the REAL winston logger throws on it inside logger.error, outside the try, so the run's promise
+// rejects with nothing logged (the timer callbacks do not await or catch it: an unhandled rejection). The guard now wraps the same expression in String(...) (the form PR 1924 merged in routes/certifications.ts), so a
+// value String() cannot read lands in the fallback and an object becomes its string form. Nothing about WHEN or WHETHER enforcement runs changes. runEnforcement is module-private, so the cells start the scheduler
+// with a 10 ms startup delay under fake timers (setImmediate stays real so a pending rejection surfaces inside the cell that caused it) and let the first scheduled run fire. The cells that name the real logger send
+// logger.error through it (its transports' output swallowed, its formats still run); the jest.fn logger of the other cells cannot reproduce the failure, because it never formats its arguments.
+const mockEnforceRetention = jest.fn();
+const mockLoggerError = jest.fn();
+const mockLoggerInfo = jest.fn();
+
+jest.mock('../services/gdprService', () => ({
+  enforceRetention: mockEnforceRetention,
+}));
+
+jest.mock('../utils/logger', () => ({
+  logger: { info: mockLoggerInfo, warn: jest.fn(), error: mockLoggerError, debug: jest.fn() },
+}));
+
+import { startRetentionScheduler, stopRetentionScheduler } from '../services/retentionScheduler';
+
+beforeEach(() => {
+  jest.clearAllMocks();
+  jest.useFakeTimers({ doNotFake: ['setImmediate', 'nextTick'] });
+  process.env.RETENTION_STARTUP_DELAY_MS = '10';
+});
+
+afterEach(() => {
+  stopRetentionScheduler();
+  jest.clearAllTimers();
+  jest.useRealTimers();
+  delete process.env.RETENTION_STARTUP_DELAY_MS;
+});
+
+async function firstRun(): Promise<void> {
+  startRetentionScheduler();
+  jest.advanceTimersByTime(10);
+  for (let i = 0; i < 20; i++) await Promise.resolve();
+  await new Promise<void>((resolve) => setImmediate(resolve));
+}
+
+async function runWithThrow(thrown: unknown): Promise<void> {
+  mockEnforceRetention.mockRejectedValueOnce(thrown);
+  await firstRun();
+}
+
+function revokedProxy(): object {
+  const { proxy, revoke } = Proxy.revocable({}, {});
+  revoke();
+  return proxy;
+}
+
+
+function messageGetterReturningRevokedProxy(): Error {
+  const e = new Error('ks1868 hidden');
+  Object.defineProperty(e, 'message', {
+    get(): unknown {
+      return revokedProxy();
+    },
+  });
+  return e;
+}
+
+function messageGetterReturningThrowingToJson(): Error {
+  const e = new Error('ks1868 hidden');
+  Object.defineProperty(e, 'message', {
+    get(): unknown {
+      return {
+        toJSON(): never {
+          throw new Error('ks1868 toJSON threw');
+        },
+      };
+    },
+  });
+  return e;
+}
+
+function useRealLogger(): void {
+  const real = jest.requireActual('../utils/logger').logger;
+  real.transports.forEach((t: { log?: (info: unknown, next: () => void) => void }) => {
+    t.log = (_info: unknown, next: () => void) => next();
+  });
+  mockLoggerError.mockImplementation((...a: unknown[]) => (real.error as (...x: unknown[]) => unknown)(...a));
+}
+
+// The logged value must already be a string when the logger is called (a typeof check, so that a hostile object is never printed by the assertion itself).
+const loggedTypes = (): string[] => mockLoggerError.mock.calls.map((c) => typeof (c[1] as { error?: unknown }).error);
+
+describe('KS-1868 retention scheduler reads a hostile message safely', () => {
+  afterEach(() => {
+    mockLoggerError.mockReset();
+  });
+
+  it('control ks1868 C1 runEnforcement: an ordinary Error logs its own message', async () => {
+    await runWithThrow(new Error('ks1868 ordinary'));
+    expect(mockEnforceRetention).toHaveBeenCalledTimes(1);
+    expect(mockLoggerError.mock.calls).toEqual([['Scheduled enforcement failed', { error: 'ks1868 ordinary' }]]);
+  });
+
+  it('control ks1868 C2 runEnforcement: an ordinary Error through the real logger logs its own message', async () => {
+    useRealLogger();
+    await runWithThrow(new Error('ks1868 ordinary'));
+    expect(mockEnforceRetention).toHaveBeenCalledTimes(1);
+    expect(loggedTypes()).toEqual(['string']);
+    expect(mockLoggerError.mock.calls).toEqual([['Scheduled enforcement failed', { error: 'ks1868 ordinary' }]]);
+  });
+
+  it('RED ks1868 R1 runEnforcement: an Error whose message getter returns a revoked Proxy is logged as the constant reason through the real logger', async () => {
+    useRealLogger();
+    await runWithThrow(messageGetterReturningRevokedProxy());
+    expect(mockEnforceRetention).toHaveBeenCalledTimes(1);
+    expect(loggedTypes()).toEqual(['string']);
+    expect(mockLoggerError.mock.calls).toEqual([['Scheduled enforcement failed', { error: 'unreadable thrown value' }]]);
+  });
+
+  it('RED ks1868 R2 runEnforcement: an Error whose message getter returns an object with a throwing toJSON is logged as its string form through the real logger', async () => {
+    useRealLogger();
+    await runWithThrow(messageGetterReturningThrowingToJson());
+    expect(mockEnforceRetention).toHaveBeenCalledTimes(1);
+    expect(loggedTypes()).toEqual(['string']);
+    expect(mockLoggerError.mock.calls).toEqual([['Scheduled enforcement failed', { error: '[object Object]' }]]);
+  });
+});
```
