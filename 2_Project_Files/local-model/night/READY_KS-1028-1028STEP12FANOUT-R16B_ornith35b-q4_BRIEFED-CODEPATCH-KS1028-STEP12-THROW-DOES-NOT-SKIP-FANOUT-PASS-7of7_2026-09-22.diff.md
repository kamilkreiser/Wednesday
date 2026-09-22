# READY — KS-1028-1028STEP12FANOUT-R16B (Ornith, briefed, code_patch, jest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1028-ornith35b-night/out.md.checker/patch.diff`** (from `ls` at 13:16 2026-09-22; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1028-ornith35b-night/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1028-ornith35b-night/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; CONTENT-compared against the drafter's golden `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_feed11-drafter-precheck/STEP12FANOUT/out.md.checker/patch.diff` (bytes DIFFER: `cmp` rc 1); file headers DIFFER (run ['+++ b/services/originate/src/services/gdprService.ts', '+++ b/services/originate/src/__tests__/ks1028-step12-throw-does-not-skip-fanout.test.ts'] vs golden ['+++ b/Blockchain/Dev/services/originate/src/services/gdprService.ts', '+++ b/Blockchain/Dev/services/originate/src/__tests__/ks1028-step12-throw-does-not-skip-fanout.test.ts']); APPLIED RESULT not compared (input.json['files'] lacks a touched file's tip content).

**Held 13:16 2026-09-22 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1028-ornith35b-night/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `8c2f7b3fd4fde915b2a24542bc32259b24e092a0`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 touched-file set == { Blockchain/Dev/services/originate/src/services/gdprService.ts , Blockchain/Dev/services/originate/src/__tests__/ks1028-step12-throw-does-not-skip-fanout.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/originate/src/services/gdprService.ts` (product) and `Blockchain/Dev/services/originate/src/__tests__/ks1028-step12-throw-does-not-skip-fanout.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
5	3	Blockchain/Dev/services/originate/src/services/gdprService.ts
99	0	Blockchain/Dev/services/originate/src/__tests__/ks1028-step12-throw-does-not-skip-fanout.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the product hunk (5 line(s)), and no tip line is re-added as a '+' (A3d)` — product section `+` lines 5 ordered-equal (whitespace-stripped) to the brief's `expected_plus` (ASCII); `-` lines 3.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: every '+' line the brief adds is in the applied Blockchain/Dev/services/originate/src/services/gdprService.ts byte-exact incl. leading whitespace (apply mode strict): OK 5 line(s) byte-exact incl. leading whitespace (of 5; 5 line(s) added by the apply)` [a3i_indent.out: `OK 5 line(s) byte-exact incl. leading whitespace (of 5; 5 line(s) added by the apply)`]
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `services/originate/src/services/gdprService.ts` (hunks=2, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `--directory=Blockchain/Dev`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `services/originate/src/__tests__/ks1028-step12-throw-does-not-skip-fanout.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `--directory=Blockchain/Dev`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: src/__tests__/ks1028-step12-throw-does-not-skip-fanout.test.ts fails at the untouched tip (2 failed / 4 run; controls green; assertion reds)` [red_first.json: failed=2 of total=4; red cell(s): ['KS-1028: a step-12 throw does not skip the USER_ERASED fan-out RED KS-1028 A: when the DSR status write throws after the shred, user.erased is STILL published', 'KS-1028: a step-12 throw does not skip the USER_ERASED fan-out RED KS-1028 B: the fan-out fires AFTER the shred, and the shred is not repeated']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: src/__tests__/ks1028-step12-throw-does-not-skip-fanout.test.ts passes with the product hunk (4 passed / 4 run)` [green_after.json: failed=0 of total=4, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=835 failed=0 | after: total=839 failed=0` · `NEW reds: []` [baseline_suite.json total=835 failed=0; after_suite.json total=839 failed=0]
- A6 [verbatim]: `PASS A6 whole services/originate suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/originate: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 +104/-3 test=src/__tests__/ks1028-step12-throw-does-not-skip-fanout.test.ts red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/originate/src/services/gdprService.ts` (+5/-3 per numstat.out) and the test file `Blockchain/Dev/services/originate/src/__tests__/ks1028-step12-throw-does-not-skip-fanout.test.ts` (+99/-0); two files. Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1 --directory=Blockchain/Dev`; section 2 `section_2.diff`: `git apply -p1 --directory=Blockchain/Dev` — at the tip `8c2f7b3fd4fde915b2a24542bc32259b24e092a0` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1028-ornith35b-night/input.json`. brief NOT LOCATED under night/briefs/ (no claim made). Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1028-ornith35b-night/checker.out`.

```diff
--- a/services/originate/src/services/gdprService.ts
+++ b/services/originate/src/services/gdprService.ts
@@ -858,5 +858,7 @@
     // 12. Mark DSR as completed
-    await updateDSRStatus(dsrId, 'completed', performedBy, `Erasure completed. ${logs.length} data types processed.`);
-
+    // KS-1028: a step-12 throw must not skip the step-13 fan-out below - captured here, re-raised after it.
+    const step12Error: unknown = await updateDSRStatus(dsrId, 'completed', performedBy, 'Erasure completed. ' + logs.length + ' data types processed.')
+      .then(() => undefined, (err: unknown) => err ?? new Error('KS-1028: step 12 rejected'));
+    // KS-1028: the fan-out (step 13) runs next; the captured error is thrown after it, before the completed log.
     // 13. Audit 2.2: fan out to other services. Originate's executeErasure
     // only touches originate's own DB; downstream services (auth, kyc, m365,
@@ -893,5 +893,5 @@
       logger.warn('Failed to publish user.erased event (cascade may be incomplete)', { userId, error: err?.message });
     }
-
+    if (step12Error) throw step12Error; // KS-1028: re-raised only AFTER the fan-out; the outer catch below still answers success false
     logger.info('Erasure completed', { userId, dataTypesProcessed: logs.length, totalRecordsAffected: logs.reduce((sum, l) => sum + l.recordsAffected, 0) });
     return { success: true, deletionLog: logs };
--- /dev/null
+++ b/services/originate/src/__tests__/ks1028-step12-throw-does-not-skip-fanout.test.ts
@@ -0,0 +1,99 @@
+// KS-1028 (KS-754 gate F-1, MAJOR): a step-12 throw in executeErasureImpl must NOT skip
+// the step-13 USER_ERASED fan-out that runs AFTER the crypto-shred (step 11). Before the
+// fix a rejected updateDSRStatus jumped straight to the outer catch, so the DEK was gone
+// and no downstream service ever heard about it. The mocks are the erasure driver's
+// (gdprService.erasure.test.ts) copied whole; only the step-12 UPDATE is made to throw,
+// matched with indexOf on the lower-cased SQL text (no regex).
+
+const mockQueryRaw = jest.fn();
+const mockExecuteRaw = jest.fn();
+
+jest.mock('../db', () => ({
+  prisma: {
+    $queryRaw: mockQueryRaw,
+    $executeRaw: mockExecuteRaw,
+  },
+}));
+
+jest.mock('../utils/logger', () => ({
+  logger: { info: jest.fn(), warn: jest.fn(), error: jest.fn(), debug: jest.fn() },
+}));
+
+jest.mock('@secuura/shared', () => require('./helpers/sharedModuleMock').makeSharedMock({
+  publishEvent: jest.fn().mockResolvedValue(undefined),
+  EventTypes: { USER_ERASED: 'user.erased' },
+  encryptField: jest.fn((v: string) => v),
+  decryptField: jest.fn((v: string) => v),
+  encryptFieldWithDek: jest.fn((v: string) => v),
+  decryptFieldWithDek: jest.fn((v: string) => v),
+  isSubjectDekCiphertext: jest.fn(() => false),
+  isEncryptedPii: jest.fn(() => false),
+  runWithPlatformScope: jest.fn(<T,>(fn: () => T): T => fn()),
+  SubjectDekProvider: class { getOrCreateDek = async () => Buffer.alloc(32); getDek = async () => null; destroyDek = async () => 'destroyed'; evict = () => undefined; },
+}));
+
+const mockDestroyDek = jest.fn().mockResolvedValue('destroyed');
+jest.mock('../services/subjectDeks', () => ({
+  subjectDeks: {
+    getOrCreateDek: jest.fn(async () => Buffer.alloc(32)),
+    getDek: jest.fn(async () => null),
+    destroyDek: mockDestroyDek,
+    evict: jest.fn(),
+  },
+}));
+
+const mockLocalPublish = jest.fn().mockResolvedValue(undefined);
+jest.mock('../events', () => ({
+  publishEvent: mockLocalPublish,
+  EventTypes: { USER_ERASED: 'user.erased' },
+}));
+
+import { executeErasure } from '../services/gdprService';
+
+/** Every executeRaw succeeds except the step-12 UPDATE of data_subject_requests, which throws. */
+function failStep12(): void {
+  mockExecuteRaw.mockImplementation(async (strings: readonly string[]) => {
+    const sql = strings.join(' ? ').toLowerCase();
+    if (sql.indexOf('update data_subject_requests') >= 0) throw new Error('step-12 boom (KS-1028)');
+    return 1;
+  });
+}
+
+const USER_ID = '11111111-1111-1111-1111-111111111111';
+const DSR_ID = '22222222-2222-2222-2222-222222222222';
+const ADMIN_ID = '33333333-3333-3333-3333-333333333333';
+
+describe('KS-1028: a step-12 throw does not skip the USER_ERASED fan-out', () => {
+  beforeEach(() => {
+    jest.clearAllMocks();
+    mockExecuteRaw.mockResolvedValue(1);
+    mockQueryRaw.mockResolvedValue([{ id: 'log-row', records_affected: 1 }]);
+  });
+
+  it('RED KS-1028 A: when the DSR status write throws after the shred, user.erased is STILL published', async () => {
+    failStep12();
+    await executeErasure(USER_ID, DSR_ID, ADMIN_ID);
+    expect(mockDestroyDek).toHaveBeenCalledWith(USER_ID);
+    expect(mockLocalPublish).toHaveBeenCalledWith('user.erased', expect.objectContaining({ userId: USER_ID, dsrId: DSR_ID }));
+  });
+
+  it('RED KS-1028 B: the fan-out fires AFTER the shred, and the shred is not repeated', async () => {
+    failStep12();
+    await executeErasure(USER_ID, DSR_ID, ADMIN_ID);
+    expect(mockDestroyDek).toHaveBeenCalledTimes(1);
+    expect(mockLocalPublish).toHaveBeenCalledTimes(1);
+    expect(mockDestroyDek.mock.invocationCallOrder[0]).toBeLessThan(mockLocalPublish.mock.invocationCallOrder[0]);
+  });
+
+  it('control: the step-12 failure still fails the erasure (success false), before and after', async () => {
+    failStep12();
+    const result = await executeErasure(USER_ID, DSR_ID, ADMIN_ID);
+    expect(result.success).toBe(false);
+  });
+
+  it('control: with no failure the erasure succeeds and publishes once', async () => {
+    const result = await executeErasure(USER_ID, DSR_ID, ADMIN_ID);
+    expect(result.success).toBe(true);
+    expect(mockLocalPublish).toHaveBeenCalledTimes(1);
+  });
+});
```
