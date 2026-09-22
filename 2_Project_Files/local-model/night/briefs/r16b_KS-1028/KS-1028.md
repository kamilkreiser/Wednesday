# KS-1028 R16B-STEP12FANOUT - Wednesday's task for Ornith: a step-12 throw in `executeErasureImpl` must not skip the step-13 USER_ERASED fan-out that runs AFTER the crypto-shred - capture the rejection, run the fan-out, re-raise (code_patch, JEST; re-brief of the STALE READY_KS-1028 at develop 8c2f7b3fd, written 12:35:22 AEST on 2026-09-22 by Wednesday's feed11 drafter from the file at the tip - `gdprService.ts` :326-:352 and :845-:900 read; the reference test `gdprService.erasure.test.ts` present at the tip)
Tip: `8c2f7b3fd4fde915b2a24542bc32259b24e092a0`
Runner: `jest`

## Premises (measured by the feed11 drafter in a `--shared --no-checkout` scratchpad clone detached at the tip; Wednesday re-derives before queueing)
- Source READY: `night/READY_KS-1028_ornith35b-q4_JEST-PASS-7of7_2026-09-15.diff.md` (Ornith PASS 7/7 at develop 48e65c435; paths lacked the `Blockchain/Dev/` prefix). Wednesday chose option (b) on 2026-09-15 22:47 (capture step 12, run the fan-out, re-raise into the existing outer catch) over option (a) (mark the DSR completed before the shred) - that choice stands; say so in the PR.
- The product at the tip is UNCHANGED since the old brief (offset 0): `:858` `    // 12. Mark DSR as completed`, `:859` the `await updateDSRStatus(...)` call, `:860` blank, `:861`-`:863` the step-13 comment, `:893` the `logger.warn('Failed to publish user.erased event ...` line, `:894` `    }`, `:895` blank, `:896` the `logger.info('Erasure completed', ...` line, `:897` `    return { success: true, deletionLog: logs };`, `:898` `  } catch (err: any) {` - all byte-exact at 8c2f7b3fd (the file is 1540 lines).
- `updateDSRStatus` (`:326`-`:352`) returns `Promise<boolean>` and RETHROWS a DB error by design (KS-754: "a failed write must NOT come back as an ordinary `false`"), so a step-12 rejection reaches `executeErasureImpl`'s outer catch at `:898` - AFTER step 11 destroyed the subject DEK (`:855`) and BEFORE step 13 published `USER_ERASED` (`:880`-`:894`). That is the defect.
- The old READY's test file is ABSENT at the tip (no `ks1028*` under `services/originate/src/__tests__/`). `gdprService.ts` is in Seat B's lane (originate) but NO round-18 PR and NO held R15/R16 READY touches it (seat_grep 0 / held_pool 0 on `gdprService.ts`, re-measured this feed). Ticket KS-1028: Backlog, not archived, no PR attached (board read at drafting time).
- The old READY's shape (a `try { await updateDSRStatus(...) } catch` that RE-ADDS the call as a `+` line) is REFUSED by the builder's context-as-addition gate, and its hunks used BLANK context lines (`:860`, `:895`), which the fence-shape gate refuses. This brief RE-CUTS both hunks: E1 replaces `:859` AND the blank `:860` (the spacer becomes a KS-1028 comment line, so the trailing context is the non-blank step-13 comment); E2 replaces the blank `:895` with the re-raise line. Same behaviour as the old READY; different bytes; no blank line anywhere in either fence.
- The test is REWRITTEN so every `+` line is ASCII, backslash-free and double-quote-free: the step-12 matcher is `indexOf` on the lower-cased SQL (no regex), the red cells carry ASCII `RED KS-1028 A/B` titles declared under `## Red cells`. The two `$queryRaw` / `$executeRaw` keys are Prisma's own names (2 `+` lines carry `$`; unavoidable). Same four cells, same meaning as the old READY.

## What is wrong (one paragraph)
`executeErasureImpl` (`Blockchain/Dev/services/originate/src/services/gdprService.ts:545`-`:901`) runs its data steps in order: step 11 CRYPTO-SHREDS the subject's DEK (`:855` `    const shredResult = await subjectDeks.destroyDek(userId);`), step 12 marks the DSR completed (`:859`, the `await updateDSRStatus(dsrId, 'completed', performedBy, ...)` call whose message is a template literal), step 13 publishes the `USER_ERASED` fan-out (`:880`-`:894`, inside its own try/catch). Because `updateDSRStatus` rethrows a DB error, a step-12 throw jumps to the outer catch at `:898` and step 13 NEVER runs: the DEK is destroyed (local data is unrecoverable) but auth, kyc, m365, wallet-connector and security audit are never told - the KS-754 gate's F-1 MAJOR finding. Fix (option b): capture the step-12 rejection instead of letting it escape, let step 13 run, then re-raise the captured error immediately before the `'Erasure completed'` log so the existing outer catch still turns it into `{ success: false }`. NOT in this task: `updateDSRStatus` itself, `routes/gdpr.ts`, KS-1031 (F-4, deploy condition), the fan-out's own try/catch.

## The exact change - TWO edits in `Blockchain/Dev/services/originate/src/services/gdprService.ts`, each its own hunk (headers `@@ -858,5 +858,7 @@` and `@@ -893,5 +893,5 @@`); no blank context line anywhere
E1 - lines 859 AND 860 replaced (2 `-` lines: the call and the blank spacer; 4 `+` lines): leading context `:858`, trailing context `:861`-`:862` - copied from the file byte for byte, each with its leading space. The call is rewritten with string concatenation (no template literal, no `$`) and a `.then(onFulfilled, onRejected)` capture; the blank spacer becomes a comment so no context line is blank.
```
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
```
E2 - line 895 (the blank line between the fan-out's closing `    }` and the `'Erasure completed'` log) replaced by the re-raise (1 `-` blank line, 1 `+` line): leading context `:893`-`:894`, trailing context `:896`-`:897`.
```
@@ -893,5 +893,5 @@
       logger.warn('Failed to publish user.erased event (cascade may be incomplete)', { userId, error: err?.message });
     }
-
+    if (step12Error) throw step12Error; // KS-1028: re-raised only AFTER the fan-out; the outer catch below still answers success false
     logger.info('Erasure completed', { userId, dataTypesProcessed: logs.length, totalRecordsAffected: logs.reduce((sum, l) => sum + l.recordsAffected, 0) });
     return { success: true, deletionLog: logs };
```
Do not touch any other line of the product file. `:891` (the `'user.erased event published'` log) carries an em-dash: it is NOT a context line of either hunk - do not include it. The `-` line at `:859` is copied byte for byte (it keeps its backticks and `${logs.length}`); the two blank `-` lines are a lone `-` with nothing after it. Old sides: 5 and 5 lines; new sides: 7 and 5.

## THIS IS JEST, NOT VITEST
`repo.test_runner` begins with `jest` (ts-jest). `describe/it/expect/beforeEach` are globals; `jest.fn` / `jest.mock` (auto-hoisted); NO `vi.*`, NO `import ... from 'vitest'`. The `@secuura/shared` mock goes through `./helpers/sharedModuleMock` exactly as the reference test does.

## The test - one NEW jest file, the erasure driver's mock shape (`gdprService.erasure.test.ts`) copied whole; only the step-12 UPDATE is made to throw
File: `Blockchain/Dev/services/originate/src/__tests__/ks1028-step12-throw-does-not-skip-fanout.test.ts`
NEW FILE: `--- /dev/null` then `+++ b/Blockchain/Dev/services/originate/src/__tests__/ks1028-step12-throw-does-not-skip-fanout.test.ts`, ONE hunk header `@@ -0,0 +1,N @@` where N is the number of `+` lines (count them: 99), every line with a leading `+`. Copy every line byte for byte - single quotes only, no double-quote character, no backslash, ASCII only (the two `$queryRaw` / `$executeRaw` property names are the only `$`).
```
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
Cells (every cell RED or CONTROL, nothing optional):
- RED `it('RED KS-1028 A: when the DSR status write throws after the shred, user.erased is STILL published')` - at the untouched tip the step-12 rejection escapes to the outer catch before step 13, so `mockLocalPublish` is never called and `toHaveBeenCalledWith('user.erased', ...)` fails by assertion; after E1+E2 the fan-out runs, then the captured error is re-raised.
- RED `it('RED KS-1028 B: the fan-out fires AFTER the shred, and the shred is not repeated')` - at the tip `mockLocalPublish` has 0 calls (`toHaveBeenCalledTimes(1)` fails by assertion); after the fix 1 call, and its invocation order is after `mockDestroyDek`'s.
- CONTROL `it('control: the step-12 failure still fails the erasure (success false), before and after')` - the outer catch answers `{ success: false }` on both trees (at the tip directly; after the fix via the E2 re-raise).
- CONTROL `it('control: with no failure the erasure succeeds and publishes once')` - the happy path on both trees.

## Red cells
- RED KS-1028 A: when the DSR status write throws after the shred, user.erased is STILL published
- RED KS-1028 B: the fan-out fires AFTER the shred, and the shred is not repeated

## Where (parsed into the checklist - every **must change** line must appear as a `-` line in your diff)
* `:859` - **must change**: the step-12 `await updateDSRStatus(dsrId, 'completed', performedBy, ...)` call (E1's first `-` line, copied from the fence above byte for byte), replaced by the captured form
* `:858` - (correct) `    // 12. Mark DSR as completed` - stays (E1's leading context)
* `:861` - (correct) `    // 13. Audit 2.2: fan out to other services. Originate's executeErasure` - stays (E1's trailing context)
* `:894` - (correct) `    }` - stays (E2's leading context; the end of the fan-out's try/catch)
* `:896` - (correct) `    logger.info('Erasure completed', { userId, dataTypesProcessed: logs.length, totalRecordsAffected: logs.reduce((sum, l) => sum + l.recordsAffected, 0) });` - stays (E2's trailing context; the re-raise is inserted directly above it)
* `:898` - (correct) `  } catch (err: any) {` - stays (the outer catch the re-raise lands in)

## Output
Exactly ONE ```diff block with TWO files: `--- a/Blockchain/Dev/services/originate/src/services/gdprService.ts` / `+++ b/Blockchain/Dev/services/originate/src/services/gdprService.ts` (TWO hunks, headers `@@ -858,5 +858,7 @@` and `@@ -893,5 +893,5 @@`), then `--- /dev/null` / `+++ b/Blockchain/Dev/services/originate/src/__tests__/ks1028-step12-throw-does-not-skip-fanout.test.ts` (one `@@ -0,0 +1,99 @@` hunk, all `+`); paths repo-relative; every context line keeps its leading space; no `\u`, backslash or double-quote character in any `+` line; the cell titles EXACTLY as listed.
