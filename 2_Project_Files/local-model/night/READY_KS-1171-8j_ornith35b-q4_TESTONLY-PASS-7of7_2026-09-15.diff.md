# READY — KS-1171 (record 8j pin only) — Ornith ornith:35b (Q4_K_M) PASS 7/7 first run, TEST-ONLY mode, 2026-09-15 12:04 — tip develop M55 48e65c435. NO product change; the cells red under the tamper (:260 confirmed gated on polled) and are green at the tip.
# Source read by Wednesday: the three cells are the brief's. Run: /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-15_ks1171-ornith35b-night. HELD for a Secuura seat (tier 2). Closes 8j only — the mixed-window design decision stays with the ticket owner.

```diff
--- /dev/null
+++ b/services/anchoring/src/__tests__/ks1171-8j-confirmed-wins-over-polled-zero.test.ts
@@ -0,0 +1,109 @@
+/**
+ * KS-1171 — Record 8j TEST-ONLY MODE. The product file at the tip is CORRECT;
+ * `reconfirmKnownSubmission` checks `confirmation.confirmed` FIRST and only
+ * THEN maps `polled === 0` to `'unknown'`. This test exists so a future tamper
+ * of line 260 (`&& confirmation.polled !== 0`) reddens these cells — proving
+ * the ordering matters for one early "not found" then an unreachable chain.
+ */
+import { describe, it, expect, vi, beforeEach } from 'vitest';
+import { BlockfrostServerError } from '@blockfrost/blockfrost-js';
+import { createAnchorSubmitter, type AnchorSubmissionDeps, type AnchorSnapshot } from '../anchorSubmission';
+
+vi.mock('../cardano/provider', async (importOriginal) => {
+  const orig = await importOriginal<typeof import('../cardano/provider')>();
+  return { ...orig, getTransaction: vi.fn() };
+});
+import { waitForConfirmation } from '../cardano/confirmation';
+
+const TX_A = '408e72087942198b69d686401829b5b9419d018dc4cc64917283aa3cdb084994';
+const ANCHOR_ID = 'anchor_a93bd8dd-10c8-4d52-b12e-c0bff6f5c790';
+
+const INPUTS_SPENT_SHORT = () =>
+  new BlockfrostServerError({
+    status_code: 400,
+    error: 'Bad Request',
+    message: 'Transaction submission failed: ConwayMempoolFailure "All inputs are spent"',
+    url: 'x',
+  });
+
+function makeLock() {
+  let chain: Promise<unknown> = Promise.resolve();
+  return function lock<T>(fn: () => Promise<T>): Promise<T> {
+    const next = chain.catch(() => undefined).then(() => fn());
+    chain = next.catch(() => undefined);
+    return next;
+  };
+}
+
+/**
+ * Harness copied from ks726 with ONE change: the confirm dep ignores the chain
+ * entirely — injected double returns FOUND but counters say no attempt reached
+ * the chain. Under the ticket's tamper this is what makes the row rest in
+ * 'submitting' instead of 'confirmed'.
+ */
+function makeHarness(confirmResult: Awaited<ReturnType<AnchorSubmissionDeps['confirm']>>) {
+  const SEED_USER_ID = 'seed-user-k1171';
+  const row: AnchorSnapshot = {
+    id: ANCHOR_ID, status: 'pending', transactionHash: undefined, retryCount: 0,
+    metadataLabel: 674, metadataPayload: { documentId: `doc-${SEED_USER_ID}` },
+  };
+  const statusWrites: Array<Record<string, unknown>> = [];
+  const signedHashes: string[] = [];
+  const logs: Array<{ level: string; message: string; meta?: Record<string, unknown> }> = [];
+  const submit = vi.fn(async (_label: number, _payload: object, options?: { onSigned?: (txHash: string) => Promise<void> }) => {
+    if (options?.onSigned) { signedHashes.push(TX_A); await options.onSigned(TX_A); }
+    throw INPUTS_SPENT_SHORT();
+  });
+  const deps: AnchorSubmissionDeps = {
+    getAnchor: vi.fn(async () => ({ ...row })),
+    submit,
+    // INJECTED DOUBLE: ignores the chain, always reports confirmed:true regardless of polled count.
+    confirm: vi.fn(async () => ({ confirmed: true, confirmations: 1, blockNumber: 4242, slot: 99, blockHash: 'b'.repeat(64), polled: 0, errored: 3 })),
+    updateStatus: vi.fn(async (_id: string, updates: Record<string, unknown>) => {
+      statusWrites.push(updates);
+      if (typeof updates.status === 'string') row.status = updates.status as AnchorSnapshot['status'];
+      if (typeof updates.transactionHash === 'string') row.transactionHash = updates.transactionHash;
+    }),
+    bumpRetryCount: vi.fn(async () => { row.retryCount += 1; }),
+    scheduleRetry: vi.fn(),
+    log: vi.fn((level, message, meta) => { logs.push({ level, message, meta }); }),
+    withWalletLock: makeLock(),
+  };
+  const statusSeq = () => statusWrites.map(w => w.status).filter((s): s is string => typeof s === 'string');
+  const calls = (fn: unknown) => (fn as ReturnType<typeof vi.fn>).mock.calls.length;
+  return { deps, row, statusSeq, signedHashes, logs, calls };
+}
+
+describe('KS-1171 — injected confirmed:true with polled:0 must still CONFIRM the row', () => {
+  it('🔴 KS-1171 8j — an injected confirmed:true with polled 0 CONFIRMS the row', async () => {
+    const h = makeHarness({ confirmed: true, confirmations: 1, blockNumber: 4242, slot: 99, blockHash: 'b'.repeat(64), polled: 0, errored: 3 });
+    await createAnchorSubmitter(h.deps)(ANCHOR_ID);
+
+    expect(h.row.status).toBe('confirmed');
+    expect(h.row.transactionHash).toBe(TX_A);
+    expect(h.calls(h.deps.scheduleRetry)).toBe(0);
+  }, 60_000);
+
+  it('🔴 KS-1171 8j — no "never reached the chain" log when the transaction was found', async () => {
+    const h = makeHarness({ confirmed: true, confirmations: 1, blockNumber: 4242, slot: 99, blockHash: 'b'.repeat(64), polled: 0, errored: 3 });
+    await createAnchorSubmitter(h.deps)(ANCHOR_ID);
+
+    expect(h.logs.some(l => l.message.startsWith('Anchor confirmation poll never reached the chain'))).toBe(false);
+    expect(h.logs.some(l => l.message === 'Anchor confirmed on Cardano')).toBe(true);
+  }, 60_000);
+});
+
+describe('KS-1171 control — confirmed:true with polled > 0 confirms too', () => {
+  it('KS-1171 control — confirmed:true with polled 2 confirms the row too', async () => {
+    // Second harness whose stub returns polled: 2, errored: 0. Green at tip AND under tamper.
+    const SEED_USER_ID_C = 'seed-user-k1171-control';
+    const rowC: AnchorSnapshot = {
+      id: ANCHOR_ID, status: 'pending', transactionHash: undefined, retryCount: 0,
+      metadataLabel: 674, metadataPayload: { documentId: `doc-${SEED_USER_ID_C}` },
+    };
+    const logsC: Array<{ level: string; message: string }> = [];
+    const signedHashesC: string[] = [];
+    const submitC = vi.fn(async (_label: number, _payload: object, options?: { onSigned?: (txHash: string) => Promise<void> }) => {
+      if (options?.onSigned) { signedHashesC.push(TX_A); await options.onSigned(TX_A); }
+      throw INPUTS_SPENT_SHORT();
+    });
+    const depsC: AnchorSubmissionDeps = {
+      getAnchor: vi.fn(async () => ({ ...rowC })),
+      submit: submitC,
+      confirm: vi.fn(async () => ({ confirmed: true, confirmations: 1, blockNumber: 4242, slot: 99, blockHash: 'b'.repeat(64), polled: 2, errored: 0 })),
+      updateStatus: vi.fn(async (_id: string, updates: Record<string, unknown>) => {
+        if (typeof updates.status === 'string') rowC.status = updates.status as AnchorSnapshot['status'];
+        if (typeof updates.transactionHash === 'string') rowC.transactionHash = updates.transactionHash;
+      }),
+      bumpRetryCount: vi.fn(),
+      scheduleRetry: vi.fn(),
+      log: vi.fn((level, message) => { logsC.push({ level, message }); }),
+      withWalletLock: makeLock(),
+    };
+    await createAnchorSubmitter(depsC)(ANCHOR_ID);
+
+    expect(rowC.status).toBe('confirmed');
+    expect(logsC.some(l => l.message.startsWith('Anchor confirmation poll never reached the chain'))).toBe(false);
+  }, 60_000);
+});
```
