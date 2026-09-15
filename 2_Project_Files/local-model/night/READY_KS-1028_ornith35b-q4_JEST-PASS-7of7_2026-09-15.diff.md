# READY — KS-1028 (KS-754 gate F-1 MAJOR: a step-12 throw in `executeErasureImpl` skipped the USER_ERASED fan-out AFTER the crypto-shred — option (b): step 12 captured in a try/catch, the fan-out runs, the captured error is re-raised into the existing outer catch) — Ornith ornith:35b (Q4_K_M) FIRST SAMPLE (`2026-09-15_ks1028-ornith35b-night`) — checker PASS 7/7 at develop M55 `48e65c435`
# Source read by Wednesday 22:51: the product hunks are the brief's lines (a 7-line captured try/catch replacing :859; `if (step12Error) throw step12Error;` above the 'Erasure completed' log); the jest test copies the erasure driver's mocks whole and fails ONLY the `UPDATE data_subject_requests` statement — 2 🔴 cells red BY ASSERTION at the tip (fan-out never published; shred-before-publish order), 2 controls green both trees (success stays false on a step-12 throw; the happy path publishes once); no new suite reds, tsc rc 0.
# PR NOTES for the raising seat: (1) Wednesday CHOSE option (b) over (a) — (a) would mark a DSR completed before the shred ran; say so in the PR and on the ticket; (2) the KS-1031 deploy-condition ticket (F-4, same path) is untouched; (3) the gate report path in the ticket is the evidence to cite; (4) paths lack the `Blockchain/Dev/` prefix.

```diff
--- a/services/originate/src/services/gdprService.ts
+++ b/services/originate/src/services/gdprService.ts
@@ -856,7 +856,13 @@ async function executeErasureImpl(
     logs.push(await logDeletion(userId, dsrId, 'pii_subject_keys', 1, 'crypto-shred', `GDPR erasure request (${shredResult})`, performedBy));
 
     // 12. Mark DSR as completed
-    await updateDSRStatus(dsrId, 'completed', performedBy, `Erasure completed. ${logs.length} data types processed.`);
+    // KS-1028: a step-12 throw must not skip the step-13 fan-out — captured here, re-raised after it.
+    let step12Error: unknown;
+    try {
+      await updateDSRStatus(dsrId, 'completed', performedBy, `Erasure completed. ${logs.length} data types processed.`);
+    } catch (err) {
+      step12Error = err;
+    }
 
     // 13. Audit 2.2: fan out to other services. Originate's executeErasure
     // only touches originate's own DB; downstream services (auth, kyc, m365,
@@ -892,6 +898,7 @@ async function executeErasureImpl(
       logger.warn('Failed to publish user.erased event (cascade may be incomplete)', { userId, error: err?.message });
     }
 
+    if (step12Error) throw step12Error;
     logger.info('Erasure completed', { userId, dataTypesProcessed: logs.length, totalRecordsAffected: logs.reduce((sum, l) => sum + l.recordsAffected, 0) });
     return { success: true, deletionLog: logs };
   } catch (err: any) {
--- /dev/null
+++ b/services/originate/src/__tests__/ks1028-step12-throw-does-not-skip-fanout.test.ts
@@ -0,0 +1,104 @@
+/**
+ * =============================================================================
+ * KS-1028 — A step-12 throw does not skip the USER_ERASED fan-out AFTER the crypto-shred
+ * =============================================================================
+ */
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
+/** Every $executeRaw succeeds except the step-12 UPDATE of data_subject_requests, which throws. */
+function failStep12(): void {
+  mockExecuteRaw.mockImplementation(async (strings: readonly string[]) => {
+    if (/UPDATE\s+data_subject_requests/i.test(strings.join(' ? '))) throw new Error('step-12 boom (KS-1028)');
+    return 1;
+  });
+}
+
+const USER_ID = '11111111-1111-1111-1111-111111111111';
+const DSR_ID = '22222222-2222-2222-2222-222222222222';
+const ADMIN_ID = '33333333-3333-3333-3333-333333333333';
+
+describe('KS-1028 — a step-12 throw does not skip the USER_ERASED fan-out', () => {
+  beforeEach(() => {
+    jest.clearAllMocks();
+    mockExecuteRaw.mockResolvedValue(1);
+    mockQueryRaw.mockResolvedValue([{ id: 'log-row', records_affected: 1 }]);
+  });
+
+  it('🔴 KS-1028 — when the DSR status write throws after the shred, user.erased is STILL published', async () => {
+    failStep12();
+    await executeErasure(USER_ID, DSR_ID, ADMIN_ID);
+    expect(mockDestroyDek).toHaveBeenCalledWith(USER_ID);
+    expect(mockLocalPublish).toHaveBeenCalledWith('user.erased', expect.objectContaining({ userId: USER_ID, dsrId: DSR_ID }));
+  });
+
+  it('🔴 KS-1028 — the fan-out fires AFTER the shred, and the shred is not repeated', async () => {
+    failStep12();
+    await executeErasure(USER_ID, DSR_ID, ADMIN_ID);
+    expect(mockDestroyDek).toHaveBeenCalledTimes(1);
+    expect(mockLocalPublish).toHaveBeenCalledTimes(1);
+    expect(mockDestroyDek.mock.invocationCallOrder[0]).toBeLessThan(mockLocalPublish.mock.invocationCallOrder[0]);
+  });
+
+  it('KS-1028 control — the step-12 failure still fails the erasure (success false), before and after', async () => {
+    failStep12();
+    const result = await executeErasure(USER_ID, DSR_ID, ADMIN_ID);
+    expect(result.success).toBe(false);
+  });
+
+  it('KS-1028 control — with no failure the erasure succeeds and publishes once', async () => {
+    const result = await executeErasure(USER_ID, DSR_ID, ADMIN_ID);
+    expect(result.success).toBe(true);
+    expect(mockLocalPublish).toHaveBeenCalledTimes(1);
+  });
+});
```
