# READY — KS-1868-KS-1868-O95-P1 (spark-dsv4flash, briefed, code_patch2, jest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o95_p1_originate_lifecycle_event_repo_create_catch_guard_message/out.md.checker/patch.diff`** (from `ls` at 14:57 2026-11-03; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o95_p1_originate_lifecycle_event_repo_create_catch_guard_message/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o95_p1_originate_lifecycle_event_repo_create_catch_guard_message/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o95_p1_originate_lifecycle_event_repo_create_catch_guard_message/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o95_p1_originate_lifecycle_event_repo_create_catch_guard_message-control/out.md.checker/patch.diff` rc 0, Wednesday).

**Held 14:57 2026-11-03 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o95_p1_originate_lifecycle_event_repo_create_catch_guard_message/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `27fe5476526c4200b752449e04be689724289e6d`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/services/originate/src/repositories/lifecycleEventRepo.ts } + { Blockchain/Dev/services/originate/src/__tests__/ks1868-lifecycle-event-repo-create-catch-unreadable-throw.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/originate/src/repositories/lifecycleEventRepo.ts` (product) and `Blockchain/Dev/services/originate/src/__tests__/ks1868-lifecycle-event-repo-create-catch-unreadable-throw.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
6	1	Blockchain/Dev/services/originate/src/repositories/lifecycleEventRepo.ts
95	0	Blockchain/Dev/services/originate/src/__tests__/ks1868-lifecycle-event-repo-create-catch-unreadable-throw.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (6 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: lifecycleEventRepo.ts`
- CODE_PATCH2 (rung 3, 1 product files + 1 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/services/originate/src/repositories/lifecycleEventRepo.ts`; test(s): `Blockchain/Dev/services/originate/src/__tests__/ks1868-lifecycle-event-repo-create-catch-unreadable-throw.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/services/originate/src/repositories/lifecycleEventRepo.ts 6 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/originate/src/__tests__/ks1868-lifecycle-event-repo-create-catch-unreadable-throw.test.ts 95 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/originate/src/repositories/lifecycleEventRepo.ts` (hunks=1, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/originate/src/__tests__/ks1868-lifecycle-event-repo-create-catch-unreadable-throw.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (2 failed / 4 run; controls green; assertion reds)` [red_first.json: failed=2 of total=4; red cell(s): ['KS-1868 createLifecycleEvent reads the rejection value safely RED ks1868 R1 a revoked Proxy is rethrown as is and logged with a constant reason', 'KS-1868 createLifecycleEvent reads the rejection value safely RED ks1868 R2 an Error whose message getter throws is rethrown as is and logged with a constant reason']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 1 product section(s) (4 passed / 4 run)` [green_after.json: failed=0 of total=4, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=2385 failed=11 | after: total=2394 failed=11` · `NEW reds: []` [baseline_suite.json total=2385 failed=11; after_suite.json total=2394 failed=11]
- A6 [verbatim]: `PASS A6 whole services/originate suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/originate: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 products=1 tests=1 red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/originate/src/repositories/lifecycleEventRepo.ts` (+6/-1 per numstat.out) and the test file `Blockchain/Dev/services/originate/src/__tests__/ks1868-lifecycle-event-repo-create-catch-unreadable-throw.test.ts` (+95/-0); 2 files in all (code_patch2: products Blockchain/Dev/services/originate/src/repositories/lifecycleEventRepo.ts). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `27fe5476526c4200b752449e04be689724289e6d` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o95_p1_originate_lifecycle_event_repo_create_catch_guard_message/input.json`. Brief (given by --brief; its `# ` heading names KS-1868): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1868_o95_p1_originate_lifecycle_event_repo_create_catch_guard_message/KS-1868.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o95_p1_originate_lifecycle_event_repo_create_catch_guard_message/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/originate/src/repositories/lifecycleEventRepo.ts b/Blockchain/Dev/services/originate/src/repositories/lifecycleEventRepo.ts
--- a/Blockchain/Dev/services/originate/src/repositories/lifecycleEventRepo.ts
+++ b/Blockchain/Dev/services/originate/src/repositories/lifecycleEventRepo.ts
@@ -79,7 +79,12 @@
       )
     `;
   } catch (err: unknown) {
-    const msg = err instanceof Error ? err.message : String(err);
+    let msg: string;
+    try {
+      msg = err instanceof Error ? err.message : String(err);
+    } catch {
+      msg = 'unreadable thrown value';
+    }
     if (msg.includes('null value in column "parent_document_id"')) {
       // Subquery returned no row — document not in this tenant.
       const friendlyErr: Error & { code?: string } = new Error(
diff --git a/Blockchain/Dev/services/originate/src/__tests__/ks1868-lifecycle-event-repo-create-catch-unreadable-throw.test.ts b/Blockchain/Dev/services/originate/src/__tests__/ks1868-lifecycle-event-repo-create-catch-unreadable-throw.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/originate/src/__tests__/ks1868-lifecycle-event-repo-create-catch-unreadable-throw.test.ts
@@ -0,0 +1,95 @@
+// KS-1868: createLifecycleEvent (src/repositories/lifecycleEventRepo.ts) catches a failed INSERT, reads the thrown value as
+// `err instanceof Error ? err.message : String(err)` (unguarded), maps a NOT NULL violation to LIFECYCLE_TARGET_NOT_FOUND, and
+// otherwise logs the message and RETHROWS the original value. When the value cannot be read (a revoked Proxy throws on
+// `instanceof`; an Error whose `message` getter throws, throws on `.message`) the catch itself throws before it logs and before
+// the rethrow, so the caller gets a different error (a TypeError) than the one the database raised. The cells make the database
+// stand-in reject with such a value and assert that the SAME value is rethrown and the log line carries a reason. The database
+// and logger stand-ins are plain functions, not jest.fn(): a spy inspects what it rejects with and could itself fail on a
+// revoked Proxy before the code under test saw it. Nothing is written.
+const mockState: { toThrow: unknown; errored: unknown[][] } = {
+  toThrow: undefined,
+  errored: [],
+};
+
+jest.mock('../db', () => ({
+  prisma: {
+    $executeRaw: (..._args: unknown[]) => Promise.reject(mockState.toThrow),
+  },
+}));
+
+jest.mock('../utils/logger', () => ({
+  logger: {
+    info: () => undefined,
+    debug: () => undefined,
+    warn: () => undefined,
+    error: (...args: unknown[]) => {
+      mockState.errored.push(args);
+    },
+  },
+}));
+
+import { createLifecycleEvent } from '../repositories/lifecycleEventRepo';
+
+const TENANT = '11111111-2222-3333-4444-555555555555';
+
+beforeEach(() => {
+  mockState.toThrow = undefined;
+  mockState.errored.length = 0;
+});
+
+const revokedProxy = (): unknown => {
+  const { proxy, revoke } = Proxy.revocable({}, {});
+  revoke();
+  return proxy;
+};
+
+const getterThrows = (): unknown =>
+  Object.create(Error.prototype, {
+    message: {
+      get() {
+        throw new Error('getter boom');
+      },
+    },
+  });
+
+/** Whether createLifecycleEvent rejected, and whether it rejected with the very value the database raised. */
+async function create(): Promise<{ rejected: boolean; same: boolean }> {
+  const raised = mockState.toThrow;
+  try {
+    await createLifecycleEvent({ tenantId: TENANT, documentId: 'doc-ks1868', action: 'rename' });
+    return { rejected: false, same: false };
+  } catch (e) {
+    return { rejected: true, same: e === raised };
+  }
+}
+
+const logLine = (error: string): unknown[] => [
+  'createLifecycleEvent failed',
+  { documentId: 'doc-ks1868', action: 'rename', error },
+];
+
+describe('KS-1868 createLifecycleEvent reads the rejection value safely', () => {
+  it('control ks1868 C1 an ordinary Error is rethrown as is and logged with its own message', async () => {
+    mockState.toThrow = new Error('connection refused');
+    expect(await create()).toEqual({ rejected: true, same: true });
+    expect(mockState.errored).toEqual([logLine('connection refused')]);
+  });
+
+  it('control ks1868 C2 a thrown plain string is rethrown as is and logged as text', async () => {
+    mockState.toThrow = 'plain boom';
+    expect(await create()).toEqual({ rejected: true, same: true });
+    expect(mockState.errored).toEqual([logLine('plain boom')]);
+  });
+
+  it('RED ks1868 R1 a revoked Proxy is rethrown as is and logged with a constant reason', async () => {
+    mockState.toThrow = revokedProxy();
+    expect(await create()).toEqual({ rejected: true, same: true });
+    expect(mockState.errored).toEqual([logLine('unreadable thrown value')]);
+  });
+
+  it('RED ks1868 R2 an Error whose message getter throws is rethrown as is and logged with a constant reason', async () => {
+    mockState.toThrow = getterThrows();
+    expect(await create()).toEqual({ rejected: true, same: true });
+    expect(mockState.errored).toEqual([logLine('unreadable thrown value')]);
+  });
+});
```
